import boto3

from alertalot.entities.base_aws_entity import BaseAwsEntity
from alertalot.entities.aws_ec2_entity import AwsEc2Entity


class ArgsObject:
    """
    A wrapper for arguments passed to the Alertalot executable.
    """
    def __init__(self, args):
        self.__args = args
        
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
    def show_target(self) -> bool:
        """
        If set, execute the show instance action
        
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
    def params_file(self) -> str | None:
        """
        Path to the parameters file to load.
        Returns:
            str | None: The path to the file, or None if not provided
        """
        return self.__args.params_file
    
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

    
    def get_aws_entity(self) -> BaseAwsEntity | None:
        """
        Get the entity object based on the type of the argument passed.
        
        Returns:
            BaseAwsEntity: The entity object.
            None: If no entity ID flag found.
        """
        if self.ec2_id is not None:
            return AwsEc2Entity()
        
        return None
