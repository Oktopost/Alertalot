import os
import re
import json

import jsonschema

from alertalot.generic.file_loader import load


class Parameters:
    """
    Container for parameters used to generate an alert configuration from the config file.
    """
    
    # Extract values like $INSTANCE_ID from a parameter string
    __VARIABLE_REGEX = r"\$[a-zA-Z0-9_-]+(?![a-zA-Z0-9_-])"
    
    
    def __init__(self, parameters: dict | None = None):
        self.__arguments: dict = parameters or {}
    
    def __contains__(self, key: str) -> bool:
        """
        Check if key exists in the dictionary
        
        Args:
            key (str): The key to check
            
        Returns:
            bool: True if the key exists.
        """
        return key in self.__arguments
    
    def __getitem__(self, key: str) -> str | None:
        """
        Get a value from the parameters list by its key.
        
        Args:
            key (str): The Key of the parameter

        Returns:
            str | None: The value for this given key, or None if the key does not exist.
        """
        return self.__arguments[key] if key in self else None
    
    def __iter__(self):
        """
        Return an iterator over the parameter keys.
        
        Returns:
            iterator: An iterator over the keys in _arguments.
        """
        for key, value in self.__arguments.items():
            yield key, value
    
    
    def update(self, values) -> None:
        """
        Add new attributes. Override any existing.
        
        Args:
            values (dict | Parameters): The attributes to add.
        """
        if isinstance(values, Parameters):
            self.__arguments.update(values.__arguments)
        elif isinstance(values, dict):
            self.__arguments.update(values)
        elif values is not None:
            raise ValueError("Expecting a Parameters object or dict")
    
    def substitute(self, text: str) -> str:
        """
        Replace all $variable occurrences in the given string with their corresponding values
        from _arguments. If a variable is not found, raise a KeyError.
        
        Args:
            text (str): The input string containing $variable placeholders.

        Returns:
            str: The string with all variables replaced.

        Raises:
            KeyError: If a variable is not found in _arguments.
        """
        def replace_match(match: re.Match) -> str:
            # Remove the leading '$'
            var_name = match.group()[1:]
            
            if var_name not in self:
                raise KeyError(f"Variable '{var_name}' not found in parameters list.")
            
            return str(self[var_name])
        
        return re.sub(self.__VARIABLE_REGEX, replace_match, text)
    
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
        
        params.update(self.__arguments)
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
