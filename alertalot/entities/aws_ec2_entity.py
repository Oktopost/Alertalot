from typing import Any

import boto3

from alertalot.generic.target_type import TargetType
from alertalot.entities.base_aws_entity import BaseAwsEntity


class AwsEc2Entity(BaseAwsEntity):
    """
    Implementation of BaseAwsEntity for AWS EC2 instances.
    
    This class provides EC2-specific functionality for loading instance data,
    validating CloudWatch alarm configurations, and extracting resource values
    from EC2 instances.
    """
    
    def __init__(self) -> None:
        """
        Initialize an AwsEc2Entity instance.
        """
        super().__init__(entity_type=TargetType.EC2)
    
    
    def load_entity(self, entity_id: str) -> dict[str, any]:
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances(InstanceIds=[entity_id])
        
        try:
            return response["Reservations"][0]["Instances"][0]
        except (KeyError, IndexError) as e:
            raise ValueError("Unexpected instance data format") from e
    
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        if "InstanceId" not in resource:
            raise ValueError("Missing InstanceId property for EC2 instance")
        
        result = {
            "INSTANCE_ID": resource["InstanceId"],
        }
        
        if "Tags" in resource:
            for tag in resource['Tags']:
                if 'Key' not in tag or 'Value' not in tag:
                    continue
                
                if tag["Key"] == 'Name':
                    result["INSTANCE_NAME"] = tag["Value"]
                    break
        
        return result
    
    def get_additional_config(self) -> dict[str, Any]:
        return {
            "namespace": "AWS/EC2",
            "dimensions":
            {
                "InstanceId": "$INSTANCE_ID"
            }
        }
    
    
    def _supported_metrics(self) -> list[str]:
        return [
            "CPUUtilization",
            "DiskReadOps",
            "DiskWriteOps",
            "DiskReadBytes",
            "DiskWriteBytes",
            "NetworkIn",
            "NetworkOut",
            "NetworkPacketsIn",
            "NetworkPacketsOut",
            "StatusCheckFailed",
            "StatusCheckFailed_Instance",
            "StatusCheckFailed_System",
            "MetadataNoToken",
            "EBSReadOps",
            "EBSWriteOps",
            "EBSReadBytes",
            "EBSWriteBytes",
            "EBSIOBalance%",
            "EBSByteBalance%"
        ]
