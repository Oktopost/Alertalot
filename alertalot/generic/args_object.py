class ArgsObject:
	def __init__(self, args):
		self.__args = args
	
	@property
	def is_verbose(self) -> bool:
		return self.__args.verbose
	
	@property
	def is_dry_run(self) -> bool:
		return self.__args.dry_run
	
	@property
	def show_config(self) -> bool:
		return self.__args.show_config
	
	@property
	def test_aws(self) -> bool:
		return self.__args.test_aws
	
	@property
	def config_file(self) -> str|None:
		"""
		Path to the config file to load.
		Returns:
			str | None: The path to the file, or None if not provided

		"""
		return self.__args.config_file
	
	@property
	def region(self) -> str|None:
		"""
		The region to run on.
		
		Returns:
			str | None: The region if provided, None if not.

		"""
		return self.__args.region