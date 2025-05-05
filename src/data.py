import os
from pathlib import Path
import json

script_path = Path(__file__).parent.parent
json_path = script_path / "tasks.json"

def read_tasks_file():
    if not os.path.exists(json_path):
        return []
    
    with open(json_path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("Erreur : le fichier JSON est corrompu")
            return []


def write_tasks_file(tasks):
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)