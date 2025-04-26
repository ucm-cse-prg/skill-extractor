import pexpect.popen_spawn
import os
import sys
import subprocess
from dotenv import load_dotenv

models = {
    '3.2': [
        "Llama3.2-1B-Instruct",
        "Llama3.2-3B-Instruct",
        "Llama3.2-1B-Instruct:int4-qlora-eo8",
        "Llama3.2-1B-Instruct:int4-spinquant-eo8",
        "Llama3.2-3B-Instruct:int4-qlora-eo8",
        "Llama3.2-3B-Instruct:int4-spinquant-eo8",
        "Llama3.2-1B",
        "Llama3.2-3B"
    ],

    '3.1': [
        "Llama3.1-8B-Instruct",
        "Llama3.1-8B"
    ],

    '3.0': [
        "Llama-3-8B-Instruct"
    ]
}

load_dotenv("llama_links.env")
url_dict = {
    '3.2': os.getenv("llama3_2_id_url"),
    '3.1': os.getenv("llama3_1_id_url"),
    '3.0': os.getenv("llama3_0_id_url")
}

'''
Llama3.2-3B-Instruct
Llama3-8B-Instruct
Llama3.2-3B-Instruct:int4-spinquant-eo8
'''

'''for (ver, ids) in models.items():
    for model_id in ids:
        id_url = url_dict[ver]
        cmd = f"llama model download --source meta --model-id  {model_id}"
        verify_cmd = verify_cmd = ["llama", "model", "verify-download", "--model-id", model_id]
        
        try:
            child = pexpect.popen_spawn.PopenSpawn(cmd, encoding='utf-8')
            child.logfile = sys.stdout
            child.expect("Please provide the signed URL for model", timeout=5) 
            child.sendline(id_url)
            child.expect("[Optionally] To run MD5 checksums,", timeout=600)
            child.expect(pexpect.EOF)
            print(f"Finished download for: {id_url}")

        except pexpect.exceptions.TIMEOUT:
            print(f"\nTimeout occurred for {model_id}")

        except Exception as e:
            print(f"\nError for {model_id}: {e}")

        subprocess.run(verify_cmd, check=True)
'''
# another sanity check for hashes
for (ver, ids) in models.items():
    for model_id in ids:
        print('\n***',model_id)
        verify_cmd = verify_cmd = ["llama", "model", "verify-download", "--model-id", model_id]
        subprocess.run(verify_cmd, check=True)