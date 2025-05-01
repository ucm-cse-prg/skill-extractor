from dataclasses import dataclass, field, fields
from typing import Optional, List, Any, Tuple, Dict
from pathlib import Path
import os

@dataclass
class Config:
    # TODO: CLI args for these?
    MODEL_FN: str = "Llama-3.2-3B-Instruct-Q8_0.gguf"       # llama model of choise
    MODEL_DIR: Path = Path(os.getcwd(), "models/")          # model file path
    MODEL_FP: Path = MODEL_DIR / MODEL_FN                   # path to text files w/ proj descriptions
    CTX_FN: str = "sys_msg.txt"                             # name of context file for llm
    BASE_DATA_DIR: Path = Path(os.getcwd(), "data/")        # where all relevant data is stored
    DESC_DIR: Path = BASE_DATA_DIR / "project_descriptions" # path to text files w/ proj descriptions
    SKILLS_DIR: Path = BASE_DATA_DIR / "skill_selections"   # path to output llm skill choices

cfg = Config()