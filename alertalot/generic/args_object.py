import boto3


class ArgsObject:
    """
    A wrapper for arguments passed to the Alertalot executable.
    """
    def __init__(self, args):
        self.__args = args
        self.__args.variables = dict(args.variables)
        
        if isinstance(self.region, str):
            boto3.setup_default_session(region_name=self.region)

    
    @property
    def is_verbose(self) -> bool:
        """
        If set, output should be more verbose
        
        Returns:
            bool: True if verbose flag is set.
        """
        return self.__args.verbose
    
    @property
    def is_quiet(self) -> bool:
        """
        If set, suppress all non error output.
        
        Returns:
            bool: True if quiet flag is set.
        """
        return self.__args.quiet
    
    @property
    def show_variables(self) -> bool:
        """
        If set, execute the show variables action
        
        Returns:
            bool: True if the flag is set.
        """
        return self.__args.show_variables
    
    @property
    def show_target(self) -> bool:
        """
        If set, execute the show target action
        
        Returns:
            bool: True if the flag is set.
        """
        return self.__args.show_target
    
    @property
    def show_template(self) -> bool:
        """
        If set, load the alarms template file, validate it and print the result or errors if any found.
        
        Returns:
            bool: True if the flag is set.
        """
        return self.__args.show_template

    @property
    def create_alarms(self) -> bool:
        """
        If set, load the alarms template file, validate it and creates alarms for it

        Returns:
            bool: True if the flag is set.
        """
        return self.__args.create_alarms

    @property
    def test_aws(self) -> bool:
        """
        If set, tests whether AWS is reachable and authentication is successful.
        
        Returns:
            bool: True if the flag is set.
        """
        return self.__args.test_aws
    
    @property
    def with_trace(self) -> bool:
        """
        If set, print out the error's trace and not only the error message.
        Returns:
            bool: True if the flag is set.
        """
        return self.__args.trace
    
    @property
    def var_files(self) -> list[str]:
        """
        List of variable files to load
        
        Returns:
            list[str]: The path to the files. Empty list if none provided.
        """
        return self.__args.var_files
    
    @property
    def template_file(self) -> str | None:
        """
        Path to the alarms template file to load.
        
        Returns:
            str | None: The path to the file, or None if not provided
        """
        return self.__args.template_file
    
    @property
    def region(self) -> str | None:
        """
        The region to run on.
        
        Returns:
            str | None: The region if provided, None if not.
        
        """
        return self.__args.region
    
    @property
    def ec2_id(self) -> str|None:
        """
        The target instance.
        
        Returns:
            str | None: Instance ID, or null if not provided

        """
        return self.__args.ec2_id
    
    @property
    def variables(self) -> dict[str, str]:
        """
        A list of variables passed to the executable using the --var argument.
        
        Returns:
            dict[str, str]: List of variables.
        """
        return self.__args.variables
    
    @property
    def is_strict(self) -> bool:
        """
        If set, the alarm template must pass validation when parsing
        and displaying parameters with the --show-variables command.
        
        Returns:
            bool: True if strict flag is set.
        """
        return self.__args.strict
