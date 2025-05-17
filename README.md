# Team Genesis LLM Project Skill Extractor

This repo is dedicated to parsing the pdfs full of project descriptions (the same ones that are given to students when indicating project preferences in the survey at the beginning of the semester) and using LLMs to choose which skills are necessay to complete.

## Setup and Run

1. Download llama models variants and put them in the `models/` folder
These can be found at various huggingface repos such as:

- 3.2: https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-uncensored-GGUF
- 3.1: https://huggingface.co/bartowski/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored-GGUF

2. Change the `MODEL_FN` attr of the Config dataclass found in `utils/config.py` to match the llama variant downloaded. The default (and currently only one tested) variant is `Llama-3.2-3B-Instruct-Q8_0.gguf`

3. Ensure the project pdf files mentioned above arer in the `data/project_descriptions/` folder

**Note:** The file name should have semester associated with it in front of any other text in the filename
e.g. '23S project summaries.pdf'

4. Classic venv stuff:

```bash
python -m venv venv
.\venv\Scripts\activate     # WINDOWS
source ./venv/bin/activate  # MAC/LINUX
pip install -r requirements.txt
```

**Note:** Current executions tested with Python 3.13.1, however it is likely to still work with earlier versions (e.g. 3.10.x) as well, though not tested.

5. run `python main.py`

- results are printed in terminal and output to `output/<Config.MODEL_FN>` where each prompted project description's response is saved as it's own json file, where the semester and project title is the filename.
- each output will contain the entire list of skills with the model's rating of each skill's necessity to complete the project in an easily parsable json format

## File Structure

skill-extractor (root)/
├── data/
│   ├── project_descriptions/   # where the source pdf files to be parsed are placed, and parsed versions output to (ex below)
│   │   ├── 23S Project Summaries.pdf
│   │   ├── 23S_all_projects.json  
│   │   ├── 23S_all_projects.txt  
│   ├── skills_list.json        # master list of skills taken from the student survey
│   ├── sys_msg.txt             # llm's context/assignment file
├── models/                     # where downloaded llama model variants are placed (ex below)
│   ├── Llama-3.2-3B-Instruct-Q8_0.gguf   
├── output/                     # where llm's skill selections are output. 
│   ├── <Config.MODEL_FN>/      # outputs from the chosen llama model 
├── utils/                      # scripts
│   ├── config.py               # contains dataclass and relevant configuration info
│   ├── llm.py                  # functions directly related to model inference and setup
│   ├── parse_pdf.py            # turning pdf of projects file into json objects for each project
├── venv/
├── main.py
├── README.md
├── requirements.txt

**Note:** If a file in the repo exists but is not mentioned here, it is likely a useless project template file that is not necessary for running at this time.

## Areas of Interest for Contributions and Further Tests
- Testing other llama models
- `utils/llm.py` has the params for inferring on the model, these can be adjusted and tested for the results.
- `data/sys_msg.txt` contains the context/assignment/instructions file given the model. 