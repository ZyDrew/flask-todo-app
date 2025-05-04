import os
from pathlib import Path
import json
from Task import Task

script_path = Path(__file__).parent.parent
json_path = script_path / "tasks.json"

def read_tasks_file():
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Task(**item) for item in data]
    else:
        return []

def write_tasks_file(tasks):
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)