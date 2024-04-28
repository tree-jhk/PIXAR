import torch
import random
from collections import defaultdict


class CollaborativeBeamSearch:
    def __init__(self, data, model):
        """초기화 함수.
        
        Args:
            data: 데이터셋 객체. 학습 데이터와 매핑 정보를 포함한다.
            model: 학습된 모델 객체. 임베딩 정보를 포함한다.
        """
        self.data = data
        self.model = model
        self.all_embeddings = self.model.entity_user_embed.weight
        self.entity_id_maps = [self.data.entity_id2org, self.data.user_id2org]
        self.relation_id_maps = [self.data.relation_id2org]

    def _compute_cosine_scores(self, candidate_embeddings, reference_embedding):
        """주어진 참조 임베딩과 후보 임베딩 간의 코사인 유사도 점수를 계산합니다.
        
        Args:
            candidate_embeddings: 후보 임베딩 텐서.
            reference_embedding: 참조 임베딩 텐서.
        
        Returns:
            Tensor: 후보들과 참조 임베딩 간의 코사인 유사도 점수.
        """
        """주어진 참조 임베딩과 후보 임베딩 간의 코사인 유사도 점수 계산"""
        """Compute cosine similarity scores between the reference embedding and candidate embeddings."""
        return torch.nn.functional.cosine_similarity(candidate_embeddings, reference_embedding, dim=1)

    def _get_candidates(self, user_id, item_id, next_id, visited, only_attribute, prefix_score=0):
        """다음 확장 노드를 위한 후보와 그들의 관계 및 점수를 가져옵니다.
        
        Args:
            user_id: 사용자 ID.
            item_id: 아이템 ID.
            next_id: 다음 확장할 노드의 ID.
            visited: 방문한 노드의 집합.
            only_attribute: 속성 관계만을 대상으로 할지의 여부.
            prefix_score: 현재까지의 점수.
        
        Returns:
            tuple: 후보 노드들, 관계들, 평균 점수들.
        """
        if only_attribute:
            candidates = [element[0] for element in self.data.train_kg_dict[next_id] if element[0] not in visited and element[1] not in [0, 1]]
            relations = [element[1] for element in self.data.train_kg_dict[next_id] if element[0] not in visited and element[1] not in [0, 1]]
        else:
            candidates = [element[0] for element in self.data.train_kg_dict[next_id] if element[0] not in visited]
            relations = [element[1] for element in self.data.train_kg_dict[next_id] if element[0] not in visited]
        
        candidate_embeddings = self.all_embeddings[candidates]
        user_embedding = self.all_embeddings[user_id].unsqueeze(0)
        item_embedding = self.all_embeddings[item_id].unsqueeze(0)
        
        # 사용자와 아이템에 대한 코사인 유사도 점수 계산
        user_scores = self._compute_cosine_scores(candidate_embeddings, user_embedding)
        item_scores = self._compute_cosine_scores(candidate_embeddings, item_embedding)
        
        # 평균 코사인 유사도 점수
        average_scores = (torch.mean(torch.stack([user_scores, item_scores]), dim=0) + prefix_score).tolist()
        
        return candidates, relations, average_scores

    def _sort_beam_nodes(self, beam_nodes, num_beams, fill=False):
        """빔 노드들을 점수에 따라 정렬하고, 필요시 샘플링을 통해 채웁니다.
        
        Args:
            beam_nodes: 빔 탐색 중의 노드 리스트.
            num_beams: 유지할 빔의 수.
            fill: 빔의 수가 부족할 경우 채울지 여부.
        
        Returns:
            list: 정렬되고 필요시 채워진 빔 노드 리스트.
        """
        if fill and len(beam_nodes) < num_beams:
            if len(beam_nodes) > 0:
                sampled_nodes = random.choices(beam_nodes, k=num_beams - len(beam_nodes))
                beam_nodes.extend(sampled_nodes)
            else:
                return beam_nodes
        return sorted(beam_nodes, key=lambda x: x[3], reverse=True)[:num_beams]
    
    def _sort_beam_paths(self, beam_paths, num_beams, fill=False):
        """빔 경로들을 점수에 따라 정렬하고, 필요시 샘플링을 통해 채웁니다.
        
        Args:
            beam_paths: 빔 탐색 중의 경로 리스트.
            num_beams: 유지할 빔의 수.
            fill: 빔의 수가 부족할 경우 채울지 여부.
        
        Returns:
            list: 정렬되고 필요시 채워진 빔 경로 리스트.
        """
        if fill and len(beam_paths) < num_beams:
            if len(beam_paths) > 0:
                sampled_paths = random.choices(beam_paths, k=num_beams - len(beam_paths))
                beam_paths.extend(sampled_paths)
            else:
                return beam_paths
        return sorted(beam_paths, key=lambda x: x[-1][3], reverse=True)[:num_beams]
    
    def remove_duplicate_paths(self, paths): # 방문 순서만 다르고 방문한 노드가 같은 경로 제거
        """방문 순서만 다른 중복 경로를 제거합니다.
        
        Args:
            paths: 경로 리스트.
        
        Returns:
            list: 중복을 제거한 경로 리스트.
        """
        unique_paths = []  # 중복되지 않은 경로를 저장할 리스트
        visited_nodes_sets = set()  # 각 경로의 방문 노드 집합
        
        for path in paths:
            current_set = tuple(sorted({triplet[i] for triplet in path for i in [0, 2]}))
            if current_set not in visited_nodes_sets:
                unique_paths.append(path)
                visited_nodes_sets.add(current_set)
        return unique_paths

    def search(self, user_id, item_id, only_attribute=False, remove_duplicate=True, num_beams=100, num_hops=5):
        """빔 탐색을 수행하여 경로를 찾습니다.
        
        Args:
            user_id: 사용자 ID. (int)
            item_id: 아이템 ID. (int)
            only_attribute: 속성 관계만을 대상으로 할지의 여부.
            remove_duplicate: 중복 경로 제거 여부.
            num_beams: 빔의 수.
            num_hops: 탐색할 홉의 수.
        
        Returns:
            tuple: 유효한 경로와 모든 경로.
        """
        paths = []
        for hop in range(1, num_hops + 1):
            if hop == 1:
                visited = {user_id, item_id}
                candidates, relations, prefix_scores = self._get_candidates(user_id, item_id, user_id, visited, only_attribute=False, prefix_score=0)
                expanded_nodes = [[user_id, relation_, tail_, prefix_score_] for tail_, relation_, prefix_score_ in zip(candidates, relations, prefix_scores)]
                sorted_expanded_nodes = self._sort_beam_nodes(expanded_nodes, num_beams, fill=False)
                paths = [[tuple(triplet_info),] for triplet_info in sorted_expanded_nodes]
            elif hop < num_hops:
                candi = []
                
                for idx, path in enumerate(paths):
                    _, _, tail, prefix_score = path[-1]
                    
                    visited = set([triplet_info[2] for path_ in paths for triplet_info in path_])
                    visited.add(user_id)
                    
                    candidates, relations, prefix_scores = self._get_candidates(user_id, item_id, tail, visited, only_attribute=only_attribute, prefix_score=prefix_score)
                    
                    next_head = tail
                    expanded_nodes = [[next_head, relation_, tail_, prefix_score_] for tail_, relation_, prefix_score_ in zip(candidates, relations, prefix_scores)]
                    
                    # 하나의 빔에서 뻗어 나온 가지들 중 num_beams개 가져오기
                    fill = True if hop == num_hops - 1 else False # 마지막에서 두번째 hop에서는 부족할 경우 beam만큼 채워줌.
                    sorted_expanded_nodes = self._sort_beam_nodes(expanded_nodes, num_beams, fill=fill)
                    
                    candi.extend([path + [tuple(triplet_info)] for triplet_info in sorted_expanded_nodes])
                if remove_duplicate:
                    candi = self.remove_duplicate_paths(candi)
                paths = self._sort_beam_paths(candi, num_beams)
                
            elif hop == num_hops:
                for idx, path in enumerate(paths):
                    visited = set([triplet_info[2] for triplet_info in path])
                    visited.add(user_id)
                    _, _, tail, prefix_score = path[-1]
                    for element in self.data.train_kg_dict[tail]:
                        next_node, next_relation = element
                        if next_node == item_id:
                            final_path = path + [tuple([tail, next_relation, item_id, None])]
                            break
                    else:
                        final_path = path + [tuple([None] * 4)]
                    paths[idx] = final_path
        valid_paths = [path for path in paths if path[-1][0] != None]
        valid_paths = self.remove_duplicate_paths(valid_paths)
        return valid_paths, paths
    
    def entity_id2original_name(self, node_id):
        for id_map in self.entity_id_maps:
            if node_id in id_map:
                return id_map[node_id]
        raise Exception(f"Entity {node_id} does not Exist!")
    
    def relation_id2original_name(self, relation_id):
        for id_map in self.relation_id_maps:
            if relation_id in id_map:
                return id_map[relation_id]
        raise Exception(f"Relation {relation_id} does not Exist!")
    
    def triplet2original_name(self, triplet:tuple):
        head, relation, tail, prefix_score = triplet
        return self.entity_id2original_name(int(head)), self.relation_id2original_name(int(relation)), \
               self.entity_id2original_name(int(tail)), prefix_score
    
    def path2linearlize(self, paths, to_original_name=False):
        str_paths = []
        for path in paths:
            str_path = ''
            for idx, triplet in enumerate(path):
                head, relation, tail, _ = self.triplet2original_name(triplet) \
                                                     if to_original_name else triplet
                str_path += (f'{head} -> {relation} -> ')
                if idx == len(path) - 1:
                    prefix_score = path[idx - 1][3]
                    normalized_prefix_score = prefix_score / (len(path) - 1)
                    str_path += (f'{tail}')
                    str_paths.append((str_path, prefix_score, normalized_prefix_score))
        return str_paths
    
    def path2triplet(self, paths, to_original_name=False):
        str_paths = []
        for path in paths:
            str_path = ''
            for idx, triplet in enumerate(path):
                head, relation, tail, _ = self.triplet2original_name(triplet) \
                                                     if to_original_name else triplet
                str_path += (f'{list((head, relation, tail))}\n')
                if idx == len(path) - 1:
                    prefix_score = path[idx - 1][3]
                    normalized_prefix_score = prefix_score / (len(path) - 1)
                    str_paths.append((str_path, prefix_score, normalized_prefix_score))
        return str_paths
    
    def path2organize(self, paths, to_original_name=False):
        str_paths = []
        for path in paths:
            str_path = ''
            for idx, triplet in enumerate(path):
                head, relation, tail, _ = self.triplet2original_name(triplet) \
                                                     if to_original_name else triplet
                str_path += (f'{list((head, relation, tail))}\n')
                if idx == len(path) - 1:
                    prefix_score = path[idx - 1][3]
                    normalized_prefix_score = prefix_score / (len(path) - 1)
                    str_paths.append((str_path, prefix_score, normalized_prefix_score))
        return str_paths
    
    def item_information(self, iid):
        result = []
        meta_information = defaultdict(list)
        for eid, rid in self.data.train_kg_dict[iid]:
            if rid != 1:
                meta_information[rid].append(self.data.entity_id2org[eid])
        for rid, entity_list in meta_information.items():
            relation_name = self.data.relation_id2org[rid].replace('item_has_','').replace('_as_attribute:', '')
            entity_list_str = ' '.join(entity_list)
            result.append(f'The {relation_name} of the movie is/are {entity_list_str}.')
        return '\n'.join(result)
    
    def user_history(self, uid, max_items):
        result = []
        prefered_item_list = self.data.train_kg_dict[uid]
        if len(prefered_item_list) > max_items:
            prefered_item_list = random.sample(prefered_item_list, k=max_items)
        for idx, (prefered_iid, rid) in enumerate(prefered_item_list):
            result.append(f'{idx + 1}. ' + self.item_information(prefered_iid))
        return '\n'.join(result)