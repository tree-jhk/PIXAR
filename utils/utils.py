import random
import os
import numpy as np
import torch
from sklearn.utils import check_random_state
import openai
from openai import OpenAI
import time
import re
import json

API_MAX_RETRY = 16
API_RETRY_SLEEP = 10
API_ERROR_OUTPUT = "$ERROR$"

def setSeeds(seed=42):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    random_state = check_random_state(seed)
    np.random.default_rng(seed=seed)

def openai_api_messages(user_prompt):
    return [{"role": "user", "content": user_prompt}]

def openai_output(client, model, query):
    openai_input = openai_api_messages(query)
    model = model
    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        response = client.chat.completions.create(
            model=model,
            messages=openai_input,
            n=1,
            temperature=0,
        )
        output = response.choices[0].message.content
        try:
            response = client.chat.completions.create(
                model=model,
                messages=openai_input,
                n=1,
                temperature=0,
            )
            output = response.choices[0].message.content
            break
        except:
            print("ERROR DURING OPENAI API")
            time.sleep(API_RETRY_SLEEP)
    return output

def llm_response(args, query, is_judge=False):
    os.environ["OPENAI_API_KEY"] = args.OPENAI_API_KEY
    client = OpenAI(
        api_key=os.environ.get(args.OPENAI_API_KEY),
    )
    if is_judge:
        response = openai_output(client, model=args.judge_model, query=query)
    else:
        response = openai_output(client, model=args.llm_model, query=query)
    return response

def extract_json(text):
    match = re.search(r'\{.*?\}', text, re.S)

    if match:
        json_content = match.group(0)
        try:
            data = json.loads(json_content.replace("'", '"'))
            return data
        except json.JSONDecodeError as e:
            fixed_json = re.sub(r',\s*\}', '}', re.sub(r',\s*\]', ']', json_content))
            try:
                data = json.loads(fixed_json)
                return data
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON again: {e}")
                return None
    else:
        print("No JSON found in the response text.")
        return None

def save_to_jsonl(data_list, file_path):
    with open(file_path, 'w') as f:
        for item in data_list:
            json.dump(item, f)
            f.write('\n')