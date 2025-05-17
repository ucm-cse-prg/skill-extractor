import os
from llama_cpp import Llama
from collections.abc import Mapping
import json

from utils.config import cfg

def load_llama(n_ctx=8192, n_gpu_layers=0, n_threads=8):
    if not os.path.exists(cfg.MODEL_FP):
        raise FileNotFoundError(f"ERROR: Model not found in location specified in the config file: {cfg.MODEL_FP}")
    
    llm = Llama(
        model_path=str(cfg.MODEL_FP),
        chat_format='llama-3',
        n_ctx=n_ctx,
        n_threads=n_threads,
        n_gpu_layers=n_gpu_layers,
        f16_kv=False,   # for mixed precision
        use_mlock=True, # pin in memory to avoid swap
    )

    return llm

def tree_to_schema(node):
    """Recursively convert the skill-tree dict into a JSON schema."""
    if isinstance(node, Mapping):
        return {
            "type":  "object",
            "properties": {k: tree_to_schema(v) for k, v in node.items()},
            "required":   list(node.keys()),
            "additionalProperties": False,
        }
    else:  # leaf (boolean placeholder)
        return {
            "type": "number",
            "minimum": 0,
            "maximum": 10
        }

def query_llm(proj_title, proj_desc, llm):
    # read the system message file -> contains the llm's 'assignment' and examples
    with open(cfg.BASE_DATA_DIR / cfg.CTX_FN) as ctx_file:
        sys_msg = ctx_file.read().strip()

    # setup input and context
    prompt = f"Here is the project background, problem(s), and objective(s) for project {proj_title}:\n\n{proj_desc}"
    messages = [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": prompt}
    ]

    # read in the desired schema (based off the skills_list.json)
    # schema restricts the llm's output to a prestructured json format matching that of 'skills_list.json'
    with open(cfg.BASE_DATA_DIR / 'skills_list.json', 'r') as skill_file:
        skill_tree = json.load(skill_file)
    
    skill_tree_schema = {
        "type": "object",
        "properties": {
            "selected_skills": tree_to_schema(skill_tree)
        },
        "required": ["selected_skills"],
        "additionalProperties": False,
    }

    response_format={
        "type": "json_object",
        "schema": skill_tree_schema
    }

    # inference
    response = llm.create_chat_completion(
        messages=messages,
        response_format=response_format,
        #response_format={"type": "json_object"},
        temperature=0.6,
        top_p=0.5,
        top_k=100,
        max_tokens=1000,
    )

    try:
        res_text = response['choices'][0]['message']['content']
        res_dict = json.loads(res_text)
        print(f"\n***RESPONSE FOR {proj_title}***\n{res_dict}")
        with open(cfg.OUT_DIR / os.path.splitext(cfg.MODEL_FN)[0] / f"{proj_title}.json", 'w') as res_file:
            json.dump(res_dict, res_file, indent=2, ensure_ascii=True)

    except Exception as e:
        print(f"Error generating skills for {proj_title}: {e}")
