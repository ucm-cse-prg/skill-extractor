import os

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
        llm = load_llama()
        os.makedirs(cfg.SKILLS_DIR, exist_ok=True)
        for proj_title, proj_desc in project_descriptions_dict.items():
            print(f"Inferring on: {proj_title}")
            query_llm(proj_title, proj_desc, llm)


if __name__ == '__main__':
    main()