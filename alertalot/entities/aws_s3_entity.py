from typing import Any

import boto3

from alertalot.generic.target_type import TargetType
from alertalot.entities.base_aws_entity import BaseAwsEntity


class AwsS3Entity(BaseAwsEntity):
    """
    Implementation of BaseAwsEntity for AWS S3 buckets.
    
    This class provides S3-specific functionality for loading bucket data,
    validating CloudWatch alarm configurations, and extracting resource values
    from S3 instances.
    """
    
    def __init__(self) -> None:
        """
        Initialize an AwsS3Entity instance.
        """
        super().__init__(entity_type=TargetType.S3)
    
    
    def load_entity(self, entity_id: str) -> dict[str, any]:
        s3 = boto3.client("s3")
        try:
            location = s3.get_bucket_location(Bucket=entity_id)
            tags = s3.get_bucket_tagging(Bucket=entity_id)
            
            return {
                "Name": entity_id,
                "Location": location.get("LocationConstraint", "us-east-1"),
                "Tags": tags.get("TagSet", [])
            }
        except s3.exceptions.ClientError as e:
            raise ValueError(f"Failed to load S3 bucket data: {str(e)}") from e
    
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        if "Name" not in resource:
            raise ValueError("Missing Name property for S3")
        
        result = {
            "BUCKET_NAME": resource["Name"],
        }
        
        if "Tags" in resource:
            for tag in resource["Tags"]:
                if tag.get("Key") == "Name":
                    result["BUCKET_DISPLAY_NAME"] = tag["Value"]
                    break
        
        return result
    
    def get_additional_config(self) -> dict[str, Any]:
        return {
            "namespace": "AWS/S3",
            "dimensions": {
                "BucketName": "$BUCKET_NAME",
                "StorageType": "AllStorageTypes"
            }
        }
    
    
    def _supported_metrics(self) -> list[str]:
        return [
            "BucketSizeBytes",
            "NumberOfObjects"
        ] 
