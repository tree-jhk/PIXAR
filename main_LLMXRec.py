import os
import sys
import random
from time import time

import pandas as pd
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
from prompts.prompt_LLMXRec import LLMXRec_Prompt
from utils.utils import llm_response


def get_LLMXRec_result(args, BeamSearch, uid, iid):
    item_information=BeamSearch.item_information(iid)
    user_history = BeamSearch.user_history(uid, max_items=9)
    
    explanation_formatted = LLMXRec_Prompt.explanation_prompt.format(user=BeamSearch.data.user_id2org[uid],
                                                            item=BeamSearch.data.entity_id2org[iid],
                                                            record=user_history,
                                                            item_information=item_information)
    explanation = llm_response(args=args, query=explanation_formatted)
    
    return explanation