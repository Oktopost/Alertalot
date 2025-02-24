import os
import json
import yaml
import jsonschema

from alertalot.generic.file_loader import load


class Config:
	def __init__(self):
		self.arguments: dict = {}
	
	
	def __contains__(self, name: str) -> bool:
		"""
		Check if key exists in the dictionary
		
		Args:
			name (str): The config name to check
			
		Returns:
			bool: True if the key exists.
		"""
		return name in self.arguments
	
	
	def update(self, values: dict|None) -> None:
		"""
		Add new attributes. Override any existing.
		
		Args:
			values (dict): The attributes to add.
		"""
		if not values is None:
			self.arguments.update(values)
	
	def as_string(self) -> str:
		"""
		Return the list of attributes as a string for debug purposes.
		Returns:
		 	str: String with each attribute on a new line, in a format "key    : value".
		 		or "-empty-" string if the attributes set is empty.
		"""
		if len(self.arguments) == 0:
			return "-empty-"
		
		length = len(max(self.arguments.keys(), key=len)) + 1
		
		return os.linesep.join(f"{k.ljust(length)}: {v}" for k, v in self.arguments.items())
	
	
	@staticmethod
	def parse(file: str, region: str|None = None) -> "Config":
		"""
		Parse a config file and return the Configuration object for this file.
		
		Args:
			file (str): Path to the file to parse
			region (str|None):
				If set, the configuration of the region will be also loaded and merged into the global config.
	
		Returns:
			Config: the config settings loaded from the file
		
		"""
		config = Config()
		parsed = load(file)
		
		current_file_directory = os.path.dirname(os.path.abspath(__file__))
		full_path = os.path.join(current_file_directory, "../../schemes/config.json")
		
		with open(full_path, "r") as f:
			scheme = json.load(f)
		
		jsonschema.validate(parsed, scheme)
		
		if "global" in parsed["config"]:
			config.update(parsed["config"]["global"])
		
		if not region is None and region in parsed["config"]:
			config.update(parsed["config"][region])
		
		return config

	

