import os
import yaml


def load_yaml(path: str):
    path = os.path.abspath(path)
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load(path: str):
    return load_yaml(path)
