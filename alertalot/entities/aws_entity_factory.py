from alertalot.generic.args_object import ArgsObject
from alertalot.generic.target_type import TargetType
from alertalot.entities.base_aws_entity import BaseAwsEntity
from alertalot.entities.aws_ec2_entity import AwsEc2Entity


class AwsEntityFactory:
    """
    Factory for creating AWS entity instances.
    """
    
    
    @staticmethod
    def from_args(args: ArgsObject) -> BaseAwsEntity | None:
        """
        Create entity instance from command line arguments.
        
        Args:
            args: Command line arguments object.
            
        Returns:
            BaseAwsEntity: AWS entity instance or None if no entity can be created.
        """
        if args.ec2_id is not None:
            return AwsEc2Entity(args.ec2_id)
        
        return None
    
    @staticmethod
    def from_type(target_type: str | TargetType) -> BaseAwsEntity:
        """
        Create entity instance from target type.
        
        Args:
            target_type (str | TargetTyp): Target type name or enum.
            
        Returns:
            BaseAwsEntity: AWS entity instance.
            
        Raises:
            ValueError: If type is string and cannot be parsed as TargetType.
            NotImplementedError: If entity type is not implemented.
        """
        if isinstance(target_type, str):
            target_type = TargetType.require(target_type)
        
        match target_type:
            case TargetType.EC2:
                return AwsEc2Entity()
            
            case _:
                raise NotImplementedError(f"Missing entity type for '{target_type.value}'")
