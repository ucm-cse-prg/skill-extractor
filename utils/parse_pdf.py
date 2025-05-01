import PyPDF2
import pandas as pd
import re
import os
import json


def parse_pdf(pdf_fp, out_text_fp=None):
    """
    Read project pdf files that contain information for all projects in a semester
    Optionally save text file
    """
    text = ""
    with open(pdf_fp, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            text += page_text
            text += '\n'

    if out_text_fp: # save output parsed txt file if given output text file path
        with open(out_text_fp, "w") as proj_file:
            proj_file.write(text)

    return text

def extract_objectives(proj_file):
    i = 1
    # read project files
    with open(proj_file, "r") as pf:
        proj_text = pf.read()

    # regex is literally insane like how are people supposed to program with this stuff
    objective_matches = re.finditer(
        r"Objectives\s*(.*?)(?=\n\n|\n\s*\d+\.|\Z)", proj_text, re.DOTALL
    )
    objectives = []
    # grab all objectives and put each objective paragraph into a list
    for objective in objective_matches:
        paragraph = objective.group(1)
        objectives.append(paragraph)

    match_found_flag = True
    while match_found_flag == True:  # iterate through all projects
        # find projects matching pattern of number preceeding project title
        project_title = re.search(f"{i}\. (.*)", proj_text)
        if project_title:  # if match found (if not indicates EOF)
            # clean project title strings
            project_title_cleaned = (
                project_title.group()
                .replace("/", "")
                .replace(".", "")
                .replace("-", "")
                .replace(" ", "_")
            )
            print(project_title_cleaned, "\n", objectives[i - 1])

            # put paired project and description into their own files
            semester = os.path.basename(proj_file)[:3]
            with open(
                f"data/parsed_descriptions/{semester}_{project_title_cleaned}.txt", "w"
            ) as extract_file:
                extract_file.write(objectives[i - 1])
            i += 1

        else:
            match_found_flag = False


def extract_descriptions(parsed_txt, semester, out_json_fp=None):
    """
    Parse a Capstone-style project brief file.

    Returns
    -------
    dict
        Keys  → "1. Can Damage Detection by Vision", …  
        Values → full block of text (Background + Problem(s) + Objectives)
    """
    # normalise newlines so the regex is simpler
    text = parsed_txt.replace("\r\n", "\n")

    # project headings -> 1. Title
    # thanks GPT b/c wtf is regex this is WILD
    header_re = re.compile(r"\n\s*(\d+)\.\s+([^\n]+?)\s*\n")

    matches = list(header_re.finditer(text))
    projects = {}

    for i, match in enumerate(matches):
        start = match.end() # start of body
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        key = f"{semester}-{match.group(1)}-{match.group(2).strip()}" # semester-proj_num-proj_title
        body = text[start:end].strip() # all text assoc with proj (background, problem, objectives)
        projects[key] = body

    if out_json_fp:
        with open(out_json_fp, 'w') as desc_file:
            json.dump(projects, desc_file, indent=4)

    return projects

def table_skills():
    pattern = r"\*\*(.*?)\*\*"  # pattern to grab strings in double asterisks
    alt_pattern = (
        r"\d+\.\s*(.*?)(?=\d+\.\s*|\n|$)"  # pattern to grab strings in numbered lists
    )
    data_path = "data/project_skills/"
    files = os.listdir(data_path)  # grab file paths
    projects = [
        os.path.splitext(file)[0] for file in files
    ]  # extract fn from fps for df index
    skill_idxs = [f"Skill {i+1}" for i in range(15)]  # column headers
    skills_df = pd.DataFrame(index=projects, columns=skill_idxs)  # define dataframe

    for i, project_skill_fp in enumerate(files):  # iterate through files
        with open(data_path + project_skill_fp, "r") as project_skill_file:
            file_text = project_skill_file.read()
            skills = re.findall(
                pattern, file_text
            )  # look for skills with regex pattern

            if not skills:  # if no skills found with pattern...
                print(f"**Using alt pattern for: {project_skill_fp}")
                skills = re.findall(
                    alt_pattern, file_text
                )  # look for skills with alternate regex pattern
                if not skills:
                    print(f"*****Unable to prase skills for: {project_skill_fp}")

            for j, skill in enumerate(skills):
                skills_df.loc[projects[i], skill_idxs[j]] = skill

    print(skills_df)
    return skills_df
