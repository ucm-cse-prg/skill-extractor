import os, sys

from utils.parse_pdf import parse_pdf, extract_descriptions
from utils.llm import query_llm, load_llama
from utils import cfg

def main():
    semesters = ["23S", "23F", "22F"]
    #semesters = ["23S"]

    # parse pdf files
    for semester in semesters:
        pdf_fp = cfg.DESC_DIR / f"{semester} CSE120 Project Summaries.pdf"
        out_text_fp = cfg.DESC_DIR / f"{semester}_all_projects.txt"
        out_desc_fp = cfg.DESC_DIR / f"{semester}_all_projects.json"

        # put pdf project descriptions in master text file
        parsed_pdf_text = parse_pdf(pdf_fp, out_text_fp=out_text_fp)

        # extract objectives into dict
        project_descriptions_dict = extract_descriptions(parsed_pdf_text, semester, out_json_fp=out_desc_fp)         

        # start local server for llama inference
        llm = load_llama(n_ctx=8192, n_gpu_layers=-1, n_threads=None)

        model_name = os.path.splitext(cfg.MODEL_FN)[0]
        os.makedirs(cfg.OUT_DIR / model_name, exist_ok=True)
        for proj_title, proj_desc in project_descriptions_dict.items():
            print(f"\n\n***** Inferring on: {proj_title} *****\n")
            query_llm(proj_title, proj_desc, llm)

if __name__ == '__main__':
    main()