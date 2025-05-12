from typing import Any

import boto3

from alertalot.generic.target_type import TargetType
from alertalot.entities.abstract_aws_lb_entity import AbstractAwsLbEntity


class AwsTargetGroupEntity(AbstractAwsLbEntity):
    """
    Implementation of AbstractAwsLbEntity for AWS Target Group.
    
    This class provides Target Group-specific functionality for validating CloudWatch alarm
    configurations and extracting resource values from Target Group instances.
    """
    
    def __init__(self) -> None:
        """
        Initialize an AwsTargetGroupEntity instance.
        """
        super().__init__(entity_type=TargetType.TARGET_GROUP)
    
    def load_entity(self, entity_id: str) -> dict[str, any]:
        elbv2 = boto3.client("elbv2")
        response = elbv2.describe_target_groups(TargetGroupArns=[entity_id])
        
        try:
            return response["TargetGroups"][0]
        except (KeyError, IndexError) as e:
            raise ValueError("Unexpected target group data format") from e
    
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        if "TargetGroupArn" not in resource:
            raise ValueError("Missing TargetGroupArn property for Target Group")
        
        result = {
            "TARGET_GROUP_ARN": resource["TargetGroupArn"],
        }
        
        if "TargetGroupName" in resource:
            result["TARGET_GROUP_NAME"] = resource["TargetGroupName"]
        
        return result
    
    def get_additional_config(self) -> dict[str, Any]:
        return {
            "namespace": "AWS/ApplicationELB",
            "dimensions": {
                "TargetGroup": "$TARGET_GROUP_NAME"
            }
        }
    
    
    def _supported_metrics(self) -> list[str]:
        return [
            "RequestCount",
            "HealthyHostCount",
            "UnHealthyHostCount",
            "HTTPCode_Target_2XX_Count",
            "HTTPCode_Target_3XX_Count",
            "HTTPCode_Target_4XX_Count",
            "HTTPCode_Target_5XX_Count",
            "TargetResponseTime",
            "TargetConnectionErrorCount",
            "TargetTLSNegotiationErrorCount"
        ] 
