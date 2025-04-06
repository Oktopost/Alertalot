from typing import ClassVar

import boto3

from alertalot.entities.base_aws_entity import BaseAwsEntity
from alertalot.validation.aws_alarm_validator import AwsAlarmValidator


class AwsEc2Entity(BaseAwsEntity):
    """
    Implementation of BaseAwsEntity for AWS EC2 instances.
    
    This class provides EC2-specific functionality for loading instance data,
    validating CloudWatch alarm configurations, and extracting resource values
    from EC2 instances.
    """
    
    EC2_METRICS: ClassVar[list[str]] = [
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
    
    
    def load_entity(self, id: str) -> dict[str, any]:
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances(InstanceIds=[id])
        
        try:
            return response["Reservations"][0]["Instances"][0]
        except (KeyError, IndexError) as e:
            raise ValueError("Unexpected instance data format") from e
    
    def validate_alarm(self, validator: AwsAlarmValidator) -> dict[str, any]:
        validated_config = {
            "metric-name":          validator.validate_metric_name(allowed=AwsEc2Entity.EC2_METRICS),
            "alarm-name":           validator.validate_alarm_name(),
            "statistic":            validator.validate_statistic(),
            "period":               validator.validate_period(),
            "comparison-operator":  validator.validate_comparison_operator(),
            "threshold":            validator.validate_threshold(min_value=0.0, max_value=1.0),
            "evaluation-periods":   validator.validate_evaluation_periods(),
        }
        
        if "alarm-actions" in validator.config:
            validated_config["alarm-actions"] = validator.validate_alarm_actions()
        
        if "tags" in validator.config:
            validated_config["tags"] = validator.validate_tags()
        
        if "treat-missing-data" in validator.config:
            validated_config["treat-missing-data"] = validator.validate_treat_missing_data()
        
        if "unit" in validator.config:
            validated_config["unit"] = validator.validate_unit()
        
        return validated_config
    
    def get_resource_values(self, instance: dict) -> dict[str, str]:
        if "InstanceId" not in instance:
            raise ValueError("Missing InstanceId property for EC2 instance")
        
        result = {
            "INSTANCE_ID": instance["InstanceId"],
        }
        
        if "Tags" in instance:
            for tag in instance['Tags']:
                if 'Key' not in tag or 'Value' not in tag:
                    continue
                
                if tag["Key"] == 'Name':
                    result["INSTANCE_NAME"] = tag["Value"]
                    break
        
        return result
    
    def get_required_alarm_keys(self) -> list[str]:
        return [
            "metric-name",
            "alarm-name",
            "statistic",
            "period",
            "comparison-operator",
            "threshold",
            "evaluation-periods"
        ]
    
    def get_optional_alarm_keys(self) -> list[str]:
        return [
            "alarm-actions",
            "tags",
            "treat-missing-data",
            "unit"
        ]