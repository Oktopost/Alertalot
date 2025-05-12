from alertalot.generic.args_object import ArgsObject
from alertalot.generic.target_type import TargetType
from alertalot.entities.base_aws_entity import BaseAwsEntity
from alertalot.entities.aws_ec2_entity import AwsEc2Entity
from alertalot.entities.aws_generic_entity import AwsGenericEntity
from alertalot.entities.aws_alb_entity import AwsAlbEntity
from alertalot.entities.aws_nlb_entity import AwsNlbEntity
from alertalot.entities.aws_target_group_entity import AwsTargetGroupEntity
from alertalot.entities.aws_lambda_entity import AwsLambdaEntity
from alertalot.entities.aws_ebs_entity import AwsEbsEntity
from alertalot.entities.aws_s3_entity import AwsS3Entity
from alertalot.entities.aws_rds_entity import AwsRdsEntity


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
            return AwsEc2Entity()
        
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
            case TargetType.GENERIC:
                return AwsGenericEntity()
            case TargetType.ALB:
                return AwsAlbEntity()
            case TargetType.NLB:
                return AwsNlbEntity()
            case TargetType.TARGET_GROUP:
                return AwsTargetGroupEntity()
            case TargetType.LAMBDA:
                return AwsLambdaEntity()
            case TargetType.EBS:
                return AwsEbsEntity()
            case TargetType.S3:
                return AwsS3Entity()
            case TargetType.RDS:
                return AwsRdsEntity()
            
            case _:
                raise NotImplementedError(f"Missing entity type for '{target_type.value}'")
