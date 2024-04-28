import os
import sys
import random
from time import time

import pandas as pd
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
from prompts.prompt_PIXAR import PIXAR_Prompt
from utils.utils import llm_response


def get_PIXAR_result(args, BeamSearch, uid, iid):
    save_path = {}
    for hops in args.hops:
        valid_paths, paths = BeamSearch.search(uid, iid, 
                          only_attribute=True, remove_duplicate=True, 
                          num_beams=args.num_beams, num_hops=hops)
        print(f"{hops} hop / valid_paths: {len(valid_paths)}, total_paths: {len(paths)}")
        save_path[hops] = BeamSearch.path2linearlize(valid_paths, to_original_name=True)
    
    selected_path = []
    for hops, paths in save_path.items():
        selected_path.extend([path[0] for path in paths[:args.num_paths]])
    selected_path_str = '\n'.join(selected_path)
    
    item_information=BeamSearch.item_information(iid)
    user_history = BeamSearch.user_history(uid, max_items=9)
    path2IC_formatted = PIXAR_Prompt.path2IC_prompt.format(paths=selected_path_str,
                                                    user=BeamSearch.data.user_id2org[uid],
                                                    item=BeamSearch.data.entity_id2org[iid],
                                                    item_information=item_information)
    
    compressed_information = llm_response(args=args, query=path2IC_formatted)
    
    IC2explanation_formatted = PIXAR_Prompt.IC2explanation_prompt.format(context=compressed_information,
                                                    user=BeamSearch.data.user_id2org[uid],
                                                    item=BeamSearch.data.entity_id2org[iid],
                                                    record=user_history,
                                                    item_information=item_information)
    explanation = llm_response(args=args, query=IC2explanation_formatted)
    
    return explanation