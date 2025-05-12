from typing import Any

import boto3

from alertalot.generic.target_type import TargetType
from alertalot.entities.base_aws_entity import BaseAwsEntity


class AwsLambdaEntity(BaseAwsEntity):
    """
    Implementation of BaseAwsEntity for AWS Lambda.
    
    This class provides Lambda-specific functionality for loading function data,
    validating CloudWatch alarm configurations, and extracting resource values
    from Lambda instances.
    """
    
    def __init__(self) -> None:
        """
        Initialize an AwsLambdaEntity instance.
        """
        super().__init__(entity_type=TargetType.LAMBDA)
    
    
    def load_entity(self, entity_id: str) -> dict[str, any]:
        lambda_client = boto3.client("lambda")
        response = lambda_client.get_function(FunctionName=entity_id)
        
        try:
            return response["Configuration"]
        except KeyError as e:
            raise ValueError("Unexpected Lambda function data format") from e
    
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        if "FunctionName" not in resource:
            raise ValueError("Missing FunctionName property for Lambda")
        
        result = {
            "FUNCTION_NAME": resource["FunctionName"],
        }
        
        if "FunctionArn" in resource:
            result["FUNCTION_ARN"] = resource["FunctionArn"]
        
        return result
    
    def get_additional_config(self) -> dict[str, Any]:
        return {
            "namespace": "AWS/Lambda",
            "dimensions": {
                "FunctionName": "$FUNCTION_NAME"
            }
        }
    
    
    def _supported_metrics(self) -> list[str]:
        return [
            "Invocations",
            "Errors",
            "Duration",
            "Throttles",
            "ConcurrentExecutions",
            "UnreservedConcurrentExecutions",
            "ProvisionedConcurrencySpilloverInvocations",
            "ProvisionedConcurrencyInvocations",
            "ProvisionedConcurrencySpilloverInvocations",
            "ProvisionedConcurrencyUtilization"
        ] 
