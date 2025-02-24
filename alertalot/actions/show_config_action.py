from alertalot.generic.args_object import ArgsObject
from alertalot.generic.config import Config


def execute(run_args: ArgsObject):
	"""
	Load and print the configuration.
	
	Args:
		run_args (ArgsObject): CLI command line arguments
	
	"""
	if run_args.config_file is None:
		raise ValueError("No config file provided")
	
	if run_args.is_verbose:
		print(f"Config: {run_args.config_file}")
		
		if run_args.region is None:
			print("Region: <None>")
		else:
			print(f"Region: {run_args.region}")
		
		print()
		print("Config:")
		print("-------")
	
	config = Config.parse(run_args.config_file, run_args.region)
	
	print(config.as_string())
	
	