import os
from llama_cpp import Llama

from utils.config import cfg

def load_llama(n_ctx=4096, n_threads=8):
    if not os.path.exists(cfg.MODEL_FP):
        raise FileNotFoundError(f"ERROR: Model not found in location specified in the config file: {cfg.MODEL_FP}")
    
    llm = Llama(
        model_path=str(cfg.MODEL_FP),
        n_ctx=n_ctx,
        n_threads=n_threads,
        f16_kv=False,   # for mixed precision
        use_mlock=True, # pin in memory to avoid swap
    )

    return llm

def query_llm(proj_title, proj_desc, llm):
    # read the system message file -> contains the llm's 'assignment' and examples
    with open(cfg.BASE_DATA_DIR / cfg.CTX_FN) as ctx_file:
        sys_msg = ctx_file.read().strip()

    prompt = f"Here is the project background, problem(s), and objective(s) for project {proj_title}:\n\n{proj_desc}"
    full_prompt = f"<s>[INST] <<SYS>>\n{sys_msg}\n<</SYS>>\n{prompt}\n[/INST]"
    
    # inference
    response = llm(
        full_prompt,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repeat_penalty=1.1,
        max_tokens=1000,
    )

    try:
        res_text = response['choices'][0]['text']
        print(f"\n***RESPONSE FOR {proj_title}***\n{res_text}")

    except Exception as e:
        print(f"Error generating skills for {proj_title}: {e}")       
