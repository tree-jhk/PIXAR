import os
import sys
import random
from time import time

import pandas as pd
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim

from model.KGAT import KGAT
from parser.parser_kgat import *
from utils.log_helper import *
from utils.metrics import *
from utils.model_helper import *
from data_loader.loader_kgat import DataLoaderKGAT
from utils.utils import *
from utils.beamsearch import CollaborativeBeamSearch
from utils.get_input import *

from main_PIXAR import *
from main_LLMXRec import *
from prompts.prompt_judge import *

data_dir = {
    'yahoo_movies':'./trained_model/KGAT/yahoo_movies/data_epoch71.pkl',
}
model_dir = {
    'yahoo_movies':'./trained_model/KGAT/yahoo_movies/model_epoch71.pth',
}


def cold_start_eval_llm_system(args):
    # GPU / CPU
    device = torch.device(args.gpu if torch.cuda.is_available() else "cpu")

    # load data
    with open(data_dir[args.data_name], 'rb') as f:
        data = pickle.load(f)

    # construct model & optimizer
    model = KGAT(args, data.n_users, data.n_entities, data.n_relations)
    model = load_model(model, model_dir[args.data_name])
    model.to(device)
    
    BeamSearch = CollaborativeBeamSearch(data, model)
    UserItem = getUserItem(data)
    
    for number_of_interations in range(2, 5):
        cold_start_uid_list = UserItem.get_cold_start_uid(number_of_interations)
        
        eval_results = []
        evaluation_result_path = f'./evaluation_result/num_interaction_{number_of_interations}.jsonl'
        for n, uid in enumerate(cold_start_uid_list):
            UserItem.set_uid(is_cold_start=True, uid=uid)
            UserItem.set_iid()
            uid, iid = UserItem.get_uid(), UserItem.get_iid()
            
            PIXAR_result = get_PIXAR_result(args, BeamSearch, uid, iid)
            LLMXRec_result = get_LLMXRec_result(args, BeamSearch, uid, iid)
            
            if n % 2 == 0:
                judge_formatted = Judge_Prompt.judge_prompt.format(system_A=PIXAR_result, system_B=LLMXRec_result)
            else:
                judge_formatted = Judge_Prompt.judge_prompt.format(system_A=LLMXRec_result, system_B=PIXAR_result)
            
            judge_result = llm_response(args=args, query=judge_formatted, is_judge=True)
            judge_result_json = extract_json(judge_result)
            
            total_result = {"system_A":"PIXAR" if n % 2 == 0 else "LLMXRec",
                            "system_B":"LLMXRec" if n % 2 == 0 else "PIXAR",
                            "judge_answer":judge_result_json["Answer"],
                            "judge_reason":judge_result_json["Reasons"],
                            "uid":uid,
                            "iid":iid,
                            "PIXAR_result":PIXAR_result,
                            "LLMXRec_result":LLMXRec_result,
                            }
            eval_results.append(total_result)
            if n % 10 == 0 or n == len(cold_start_uid_list) - 1:
                save_to_jsonl(eval_results, file_path=evaluation_result_path)
            break
    
if __name__ == '__main__':
    args = parse_kgat_args()
    setSeeds(args.seed)
    cold_start_eval_llm_system(args)