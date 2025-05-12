from typing import Any

import boto3

from alertalot.generic.target_type import TargetType
from alertalot.entities.base_aws_entity import BaseAwsEntity


class AwsEbsEntity(BaseAwsEntity):
    """
    Implementation of BaseAwsEntity for AWS EBS volumes.
    
    This class provides EBS-specific functionality for loading volume data,
    validating CloudWatch alarm configurations, and extracting resource values
    from EBS instances.
    """
    
    def __init__(self) -> None:
        """
        Initialize an AwsEbsEntity instance.
        """
        super().__init__(entity_type=TargetType.EBS)
    
    
    def load_entity(self, entity_id: str) -> dict[str, any]:
        ec2 = boto3.client("ec2")
        response = ec2.describe_volumes(VolumeIds=[entity_id])
        
        try:
            return response["Volumes"][0]
        except (KeyError, IndexError) as e:
            raise ValueError("Unexpected EBS volume data format") from e
    
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        if "VolumeId" not in resource:
            raise ValueError("Missing VolumeId property for EBS")
        
        result = {
            "VOLUME_ID": resource["VolumeId"],
        }
        
        if "Tags" in resource:
            for tag in resource["Tags"]:
                if tag.get("Key") == "Name":
                    result["VOLUME_NAME"] = tag["Value"]
                    break
        
        return result
    
    def get_additional_config(self) -> dict[str, Any]:
        return {
            "namespace": "AWS/EBS",
            "dimensions": {
                "VolumeId": "$VOLUME_ID"
            }
        }
    
    
    def _supported_metrics(self) -> list[str]:
        return [
            "VolumeReadBytes",
            "VolumeWriteBytes",
            "VolumeReadOps",
            "VolumeWriteOps",
            "VolumeTotalReadTime",
            "VolumeTotalWriteTime",
            "VolumeIdleTime",
            "VolumeQueueLength",
            "VolumeThroughputPercentage",
            "VolumeConsumedReadWriteOps",
            "BurstBalance",
            "VolumeAvgReadLatency",
            "VolumeAvgWriteLatency",
            "VolumeIOPSExceededCheck",
            "VolumeStalledIOCheck",
            "VolumeThroughputExceededCheck"
        ]
