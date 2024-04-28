import os
import random
import collections

import torch
import numpy as np
import pandas as pd
import scipy.sparse as sp

from data_loader.loader_base import DataLoaderBase


class DataLoaderKGAT(DataLoaderBase):

    def __init__(self, args, logging):
        super().__init__(args, logging)
        self.cf_batch_size = args.cf_batch_size
        self.kg_batch_size = args.kg_batch_size
        self.test_batch_size = args.test_batch_size

        kg_data = self.load_kg(self.kg_file)
        self.construct_data(kg_data)
        self.print_info(logging)

        self.laplacian_type = args.laplacian_type
        self.create_adjacency_dict()
        self.create_laplacian_dict()
        
        self.load_additional_mappings()

    def load_additional_mappings(self):
        # User, Item, Entity, Relation 데이터를 불러오고, 필요한 변환을 수행합니다.
        user_list_df = pd.read_csv(os.path.join(self.data_dir, 'user_list.txt'), sep=' ')
        user_list_df['remap_id'] = user_list_df['remap_id'].astype(int)
        try:
            item_list_df = pd.read_csv(os.path.join(self.data_dir, 'item_list.txt'), sep=' ')
            item_list_df['remap_id'] = item_list_df['remap_id'].astype(int)
            
            entity_list_df = pd.read_csv(os.path.join(self.data_dir, 'entity_list.txt'), sep=' ')
            entity_list_df['remap_id'] = entity_list_df['remap_id'].astype(int)
            
            relation_list_df = pd.read_csv(os.path.join(self.data_dir, 'relation_list.txt'), sep=' ')
            relation_list_df['remap_id'] = relation_list_df['remap_id'].astype(int)
        except:
            item_list_df = pd.read_csv(os.path.join(self.data_dir, 'item_list.tsv'), sep='\t')
            item_list_df['remap_id'] = item_list_df['remap_id'].astype(int)
            
            entity_list_df = pd.read_csv(os.path.join(self.data_dir, 'entity_list.tsv'), sep='\t')
            entity_list_df['remap_id'] = entity_list_df['remap_id'].astype(int)
            
            relation_list_df = pd.read_csv(os.path.join(self.data_dir, 'relation_list.tsv'), sep='\t')
            relation_list_df['remap_id'] = relation_list_df['remap_id'].astype(int)

        # User ID를 원래의 org_id에 매핑합니다. 여기서 user_id는 entity_id와 함께 사용되므로 조정이 필요합니다.
        self.user_id2org = dict(zip(user_list_df['remap_id'] + self.n_entities, user_list_df['org_id']))
        
        # Item ID와 Freebase ID를 원래의 org_id에 매핑합니다.
        self.item_id2org = dict(zip(item_list_df['remap_id'], item_list_df['org_id']))
        try:
            self.item_id2freebase = dict(zip(item_list_df['remap_id'], item_list_df['freebase_id']))
        except:
            pass
        
        # Entity ID를 원래의 org_id에 매핑합니다.
        self.entity_id2org = dict(zip(entity_list_df['remap_id'], entity_list_df['org_id']))
        
        # Relation ID를 원래의 org_id에 매핑합니다. 역방향 관계를 고려하여, relation_id에 n_relations 만큼 더한 후 2를 더해야 합니다.
        remapped_relations = list(relation_list_df['remap_id']) + list(relation_list_df['remap_id'] + len(list(relation_list_df['remap_id'])))  # 직접 관계와 역방향 관계
        org_ids = list('item_has_' + org_id + '_as_attribute:' for org_id in relation_list_df['org_id']) + \
                  list('attribute_is_' + org_id + '_of_item:' for org_id in relation_list_df['org_id']) # 각 관계의 원래 ID를 두 번 반복
        self.relation_id2org = dict(zip([r + 2 for r in remapped_relations], org_ids))  # 모든 관계 ID에 2를 더해 최종 매핑
        self.relation_id2org[0] = 'user_likes_item'
        self.relation_id2org[1] = 'item_isLikedBy_user'

    def construct_data(self, kg_data):
        # add inverse kg data
        # kg_data: item - relation - attribute, attribute - relation - item
        n_relations = max(kg_data['r']) + 1
        inverse_kg_data = kg_data.copy()
        inverse_kg_data = inverse_kg_data.rename({'h': 't', 't': 'h'}, axis='columns')
        inverse_kg_data['r'] += n_relations
        kg_data = pd.concat([kg_data, inverse_kg_data], axis=0, ignore_index=True, sort=False)

        # re-map user id
        kg_data['r'] += 2
        self.n_relations = max(kg_data['r']) + 1
        self.n_entities = max(max(kg_data['h']), max(kg_data['t'])) + 1
        self.n_users_entities = self.n_users + self.n_entities
        
        # 유저, 좋아하는 아이템 -> 유저 id + (아이템 수 + relation 수)
        self.cf_train_data = (np.array(list(map(lambda d: d + self.n_entities, self.cf_train_data[0]))).astype(np.int32), self.cf_train_data[1].astype(np.int32))
        self.cf_test_data = (np.array(list(map(lambda d: d + self.n_entities, self.cf_test_data[0]))).astype(np.int32), self.cf_test_data[1].astype(np.int32))

        # key: 유저 id + (아이템 수 + relation 수), value: 좋아하는 아이템 list의 unique
        self.train_user_dict = {k + self.n_entities: np.unique(v).astype(np.int32) for k, v in self.train_user_dict.items()}
        self.test_user_dict = {k + self.n_entities: np.unique(v).astype(np.int32) for k, v in self.test_user_dict.items()}

        # add interactions to kg data
        # 0: user-item interaction에 대한 relation id user -> item
        cf2kg_train_data = pd.DataFrame(np.zeros((self.n_cf_train, 3), dtype=np.int32), columns=['h', 'r', 't'])
        cf2kg_train_data['h'] = self.cf_train_data[0]
        cf2kg_train_data['t'] = self.cf_train_data[1]

        # 1: item -> user
        inverse_cf2kg_train_data = pd.DataFrame(np.ones((self.n_cf_train, 3), dtype=np.int32), columns=['h', 'r', 't'])
        inverse_cf2kg_train_data['h'] = self.cf_train_data[1]
        inverse_cf2kg_train_data['t'] = self.cf_train_data[0]

        # kg랑 cf 합치기
        self.kg_train_data = pd.concat([kg_data, cf2kg_train_data, inverse_cf2kg_train_data], ignore_index=True)
        self.n_kg_train = len(self.kg_train_data)

        # construct kg dict
        '''아래는 내가 리팩토링함'''
        h_list = self.kg_train_data.loc[:, "h"].to_list()
        t_list = self.kg_train_data.loc[:, "t"].to_list()
        r_list = self.kg_train_data.loc[:, "r"].to_list()
        
        self.h_list = torch.LongTensor(h_list)
        self.t_list = torch.LongTensor(t_list)
        self.r_list = torch.LongTensor(r_list)

        self.train_kg_dict = self.kg_train_data.groupby('h').apply(lambda x: list(zip(x['t'], x['r']))).to_dict()
        self.train_relation_dict = self.kg_train_data.groupby('r').apply(lambda x: list(zip(x['h'], x['t']))).to_dict()
        
        # # construct kg dict
        # h_list = []
        # t_list = []
        # r_list = []

        # self.train_kg_dict = collections.defaultdict(list)
        # self.train_relation_dict = collections.defaultdict(list)

        # for row in self.kg_train_data.iterrows():
        #     h, r, t = row[1]
        #     h_list.append(h)
        #     t_list.append(t)
        #     r_list.append(r)

        #     self.train_kg_dict[h].append((t, r))
        #     self.train_relation_dict[r].append((h, t))

        # self.h_list = torch.LongTensor(h_list)
        # self.t_list = torch.LongTensor(t_list)
        # self.r_list = torch.LongTensor(r_list)

    def convert_coo2tensor(self, coo):
        values = coo.data
        indices = np.vstack((coo.row, coo.col))

        i = torch.LongTensor(indices)
        v = torch.FloatTensor(values)
        shape = coo.shape
        return torch.sparse.FloatTensor(i, v, torch.Size(shape))


    def create_adjacency_dict(self):
        self.adjacency_dict = {}
        for r, ht_list in self.train_relation_dict.items():
            rows = [e[0] for e in ht_list]
            cols = [e[1] for e in ht_list]
            vals = [1] * len(rows)
            # self.n_users_entities: user + item + attribute 개수
            adj = sp.coo_matrix((vals, (rows, cols)), shape=(self.n_users_entities, self.n_users_entities))
            self.adjacency_dict[r] = adj


    def create_laplacian_dict(self):
        def symmetric_norm_lap(adj):
            rowsum = np.array(adj.sum(axis=1))

            d_inv_sqrt = np.power(rowsum, -0.5).flatten()
            d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0
            d_mat_inv_sqrt = sp.diags(d_inv_sqrt)

            norm_adj = d_mat_inv_sqrt.dot(adj).dot(d_mat_inv_sqrt)
            return norm_adj.tocoo()

        def random_walk_norm_lap(adj):
            rowsum = np.array(adj.sum(axis=1))

            d_inv = np.power(rowsum, -1.0).flatten()
            d_inv[np.isinf(d_inv)] = 0
            d_mat_inv = sp.diags(d_inv)

            norm_adj = d_mat_inv.dot(adj)
            return norm_adj.tocoo()

        if self.laplacian_type == 'symmetric':
            norm_lap_func = symmetric_norm_lap
        elif self.laplacian_type == 'random-walk':
            norm_lap_func = random_walk_norm_lap
        else:
            raise NotImplementedError

        self.laplacian_dict = {}
        for r, adj in self.adjacency_dict.items():
            self.laplacian_dict[r] = norm_lap_func(adj)
        A_in = sum(self.laplacian_dict.values())
        self.A_in = self.convert_coo2tensor(A_in.tocoo())


    def print_info(self, logging):
        logging.info('n_users:           %d' % self.n_users)
        logging.info('n_items:           %d' % self.n_items)
        logging.info('n_entities:        %d' % self.n_entities)
        logging.info('n_users_entities:  %d' % self.n_users_entities)
        logging.info('n_relations:       %d' % self.n_relations)

        logging.info('n_h_list:          %d' % len(self.h_list))
        logging.info('n_t_list:          %d' % len(self.t_list))
        logging.info('n_r_list:          %d' % len(self.r_list))

        logging.info('n_cf_train:        %d' % self.n_cf_train)
        logging.info('n_cf_test:         %d' % self.n_cf_test)

        logging.info('n_kg_train:        %d' % self.n_kg_train)


