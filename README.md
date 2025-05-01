
## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)


## Project Overview

Testing various LLMs and their ability to extract programming related skill from project descriptions



eventually more stuff

## Project Structure

```

```

## Installation

1. Download gguf Llama variants of your choosing and put them in the `models` folder
- 3.1: https://huggingface.co/bartowski/DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored-GGUF
- 3.2: https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-uncensored-GGUF

2. adjust the `utils/config.py` dataclass
- mostly will just need to specify model file name

3. setup a venv and install requirements

4. if using GPU for llm inference:
- CMD: `CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir`

- Powershell: 

```
$env:CMAKE_ARGS="-DGGML_CUDA=on"
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```



## Usage

### Configuration