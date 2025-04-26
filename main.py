import os
import requests
import subprocess
import time
import signal

# --- CONFIGURATION ---
MODEL_NAME = "Llama3.2-1B-Instruct"
SERVER_URL = "http://localhost:11434"
DESC_PATH = "data/parsed_descriptions/"
SKILLS_PATH = "data/project_skills_from_list/"
SKILLS_LIST_FILE = "SKILLS_LIST.txt"

def start_llama_server(model_name):
    """Starts the llama server as a subprocess"""
    print("Starting llama server...")
    server_cmd = ["llama", "server", "--model", model_name]
    # Important: use Popen to start without blocking
    server_proc = subprocess.Popen(server_cmd)
    return server_proc

def wait_for_server_ready(url, timeout=60):
    """Polls until the server is ready or timeout happens"""
    print("Waiting for server to be ready...")
    for _ in range(timeout):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("*** Server is ready! ***")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    raise RuntimeError("Server did not become ready in time!")

def stop_llama_server(proc):
    """Stops the llama server subprocess cleanly"""
    print("Stopping llama server...")
    if proc.poll() is None:  # still running
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()

def load_skills_list(skills_list_file):
    with open(skills_list_file, "r") as skill_file:
        lines = skill_file.read()
        skill_list = [line.strip() for line in lines]
    return lines, skill_list

def main():
    # start local server
    server_proc = start_llama_server(MODEL_NAME)

    try:
        wait_for_server_ready(SERVER_URL)

        # load skills and projects
        print("Loading skills list...")
        lines, skill_list = load_skills_list(SKILLS_LIST_FILE)

        projects = os.listdir(DESC_PATH)

        prompt_prefix = (
            "given the following project description, and the following list of programming skills,"
            " choose skills, from the list of skills below, that a team of developers must possess to complete the project described."
            " Please format your answers as a numbered list."
        )

        # inference loop
        for project in projects:
            with open(os.path.join(DESC_PATH, project), "r") as description_file:
                description = description_file.read()

            formatted_prompt = f"### Human: {prompt_prefix}\nList of skills to choose from: {lines}\nProject Description: {description}\n\n### Assistant:"

            response = requests.post(
                f"{SERVER_URL}/v1/chat/completions",
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": "You are an expert software engineer tasked with selecting necessary programming skills for projects."},
                        {"role": "user", "content": formatted_prompt}
                    ],
                    "temperature": 0.7,
                    "top_p": 0.7,
                    "n": 1,
                    "max_tokens": 300,
                }
            )

            try:
                result = response.json()
                generated_text = result['choices'][0]['message']['content']
                print(f"Result for {project}: {generated_text}")

                with open(os.path.join(SKILLS_PATH, project), "w") as skill_file:
                    skill_file.write(generated_text)

            except Exception as e:
                print(f"Error generating skills for {project}: {e}")

    finally:
        # stop server
        stop_llama_server(server_proc)

if __name__ == "__main__":
    main()
