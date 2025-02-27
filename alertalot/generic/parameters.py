import os

import json
import jsonschema

from alertalot.generic.file_loader import load


class Parameters:
    """
    Container for parameters used to generate an alert configuration from the config file.
    """
    
    def __init__(self):
        self._arguments: dict = {}
    
    def __contains__(self, key: str) -> bool:
        """
        Check if key exists in the dictionary
        
        Args:
            key (str): The key to check
            
        Returns:
            bool: True if the key exists.
        """
        return key in self._arguments
    
    def __getitem__(self, key: str) -> str | None:
        """
        Get a value from the parameters list by its key.
        
        Args:
            key (str): The Key of the parameter

        Returns:
            str | None: The value for this given key, or None if the key does not exist.
        """
        return self._arguments[key] if key in self else None
    
    def update(self, values: dict | None) -> None:
        """
        Add new attributes. Override any existing.
        
        Args:
            values (dict): The attributes to add.
        """
        if values is not None:
            self._arguments.update(values)
    
    def as_string(self) -> str:
        """
        Return the list of attributes as a string for debug purposes.
        Returns:
            str: String with each attribute on a new line, in a format "key    : value".
                or "-empty-" string if the attributes set is empty.
        """
        if len(self._arguments) == 0:
            return "-empty-"
        
        length = len(max(self._arguments.keys(), key=len)) + 1
        
        return os.linesep.join(f"{k.ljust(length)}: {v}" for k, v in self._arguments.items())
    
    def merge(self, values: dict) -> "Parameters":
        """
        Creates and returns a new Parameters object by merging the values of this instance
        with those from the given dictionary.
    
        Args:
            values (dict):
                Additional values to merge.
    
        Returns:
            Parameters: A new instance containing parameters from both this instance
                and the provided dictionary.  
        """
        
        params = Parameters()
        
        params.update(self._arguments)
        params.update(values)
        
        return params
    
    
    @staticmethod
    def parse(file: str, region: str | None = None) -> "Parameters":
        """
        Parse a params file and return the Parameters object for it.
        
        Args:
            file (str): Path to the file to parse
            region (str|None):
                If set, the configuration of the region will be also loaded and merged into the global config.
        
        Returns:
            Parameters: the parameters set, loaded from the file
        """
        params = Parameters()
        parsed = load(file)
        
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_file_directory, "../../schemes/params.json")
        
        with open(full_path, "r", encoding="utf-8") as f:
            scheme = json.load(f)
        
        jsonschema.validate(parsed, scheme)
        
        if "global" in parsed["params"]:
            params.update(parsed["params"]["global"])
        
        if region is not None and region in parsed["params"]:
            params.update(parsed["params"][region])
        
        return params
