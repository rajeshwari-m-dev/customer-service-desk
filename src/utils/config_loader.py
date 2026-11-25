import os
import json
from dotenv import load_dotenv
from pathlib import Path

#Path comes from the pathlib module — it's not a Python builtin, so every file that uses it needs its own import line:
PROJECT_ROOT = Path(__file__).resolve().parent.parent 
print(PROJECT_ROOT)

def load_config(config_path : str ="config/config.json") -> dict:
    #load config files and env variab files

    load_dotenv()

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file is not found at location {config_path}")
    with open(config_path,"r") as f:
        config = json.load(f)
    return config




