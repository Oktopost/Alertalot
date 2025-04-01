import os
import json
import yaml


def load_yaml(path: str):
    """
    Loads and parses a YAML file from the specified path.
    
    Args:
        path (str): Relative or absolute path to the YAML file
        
    Returns:
        dict: Parsed YAML content as a dictionary
    """
    
    path = os.path.abspath(path)
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: str):
    """
    Loads and parses a JSON file from the specified path.
    
    Args:
        path (str): Relative or absolute path to the JSON file
        
    Returns:
        dict: Parsed JSON content as a dictionary
    """
    path = os.path.abspath(path)
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load(path: str):
    """
    Loads a configuration file from the specified path based on file extension.
    
    Supports YAML (.yaml, .yml) and JSON (.json) files.
    
    Args:
        path (str): Relative or absolute path to the config file
        
    Returns:
        dict: Parsed file content as a dictionary
        
    Raises:
        ValueError: If the file extension is not supported
    """
    path = os.path.abspath(path)
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    
    if ext in ('.yaml', '.yml'):
        return load_yaml(path)
    elif ext == '.json':
        return load_json(path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}. Supported extensions are .yaml, .yml, and .json")
