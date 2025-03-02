class ArgsObject:
    """
    A wrapper for arguments passed to the Alertalot executable.
    """
    
    def __init__(self, args):
        self.__args = args
    
    @property
    def is_verbose(self) -> bool:
        """
        If set, output should be more verbose
        
        Returns:
            bool: True if verbose flag is set.
        """
        return self.__args.verbose
    
    @property
    def is_dry_run(self) -> bool:
        """
        If set, do not execute any updates, just simulate them.
        
        Returns:
            bool: True if the dry run flag is set.
        """
        return self.__args.dry_run
    
    @property
    def show_parameters(self) -> bool:
        """
        If set, execute the show parameters action
        
        Returns:
            bool: True if the flag is set.
        """
        return self.__args.show_parameters
    
    @property
    def show_instance(self) -> bool:
        """
        If set, execute the show instance action
        
        Returns:
            bool: True if the flag is set.
        """
        return self.__args.show_instance
    
    @property
    def test_aws(self) -> bool:
        """
        If set, tests whether AWS is reachable and authentication is successful.
        
        Returns:
            bool: True if the flag is set.
        """
        return self.__args.test_aws
    
    @property
    def params_file(self) -> str | None:
        """
        Path to the parameters file to load.
        Returns:
            str | None: The path to the file, or None if not provided
        """
        return self.__args.params_file
    
    @property
    def region(self) -> str | None:
        """
        The region to run on.
        
        Returns:
            str | None: The region if provided, None if not.
        
        """
        return self.__args.region
    
    @property
    def instance_id(self) -> str | None:
        """
        The target instance.
        
        Returns:
            str | None: Instance ID, or null if not provided

        """
        return self.__args.instance_id
