import boto3

from alertalot.entities.base_aws_entity import BaseAwsEntity
from alertalot.generic.target_type import TargetType


class AbstractAwsLbEntity(BaseAwsEntity):
    """
    Abstract base class for AWS Load Balancer entities.
    
    This class provides common functionality for loading load balancer data
    and extracting resource values from load balancer instances.
    """
    
    def __init__(self, entity_type: TargetType) -> None:
        """
        Initialize an AbstractAwsLbEntity instance.
        
        Args:
            entity_type (TargetType): The type of load balancer entity.
        """
        super().__init__(entity_type=entity_type)
    
    
    def load_entity(self, entity_id: str) -> dict[str, any]:
        elbv2 = boto3.client("elbv2")
        response = elbv2.describe_load_balancers(LoadBalancerArns=[entity_id])
        
        try:
            return response["LoadBalancers"][0]
        except (KeyError, IndexError) as e:
            raise ValueError("Unexpected load balancer data format") from e
    
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        if "LoadBalancerArn" not in resource:
            raise ValueError(f"Missing LoadBalancerArn property for {self.entity_type.value}")
        
        result = {
            "LOAD_BALANCER_ARN": resource["LoadBalancerArn"],
        }
        
        if "LoadBalancerName" in resource:
            result["LOAD_BALANCER_NAME"] = resource["LoadBalancerName"]
        
        return result 
