from abc import ABC, abstractmethod
from typing import Any

from alertalot.validation.aws_alarm_validator import AwsAlarmValidator
from alertalot.generic.target_type import TargetType


class BaseAwsEntity(ABC):
    """
    Base abstract class for AWS entities that can be monitored with CloudWatch alarms.
    
    This class defines the interface that all AWS entity implementations must adhere to,
    including methods for loading entity data, validating alarm configurations, and
    extracting resource values for alarm creation.
    """
    
    def __init__(
            self,
            *,
            entity_type: TargetType.EC2):
        """
        Creates a new AWS entity instance.
        
        Args:
            entity_type (TargetType): The type of entity.
        """
        
        self.__entity_type = entity_type
    
    
    @property
    def entity_type(self) -> TargetType:
        """
        Get the entity type this entity represents.
        
        Returns:
            TargetType: The entity type this entity represents
        """
        return self.__entity_type
    
    
    @abstractmethod
    def get_resource_values(self, resource: dict) -> dict[str, str]:
        """
        Extract values from AWS resource.
        
        Args:
            resource (dict): The AWS resource
            
        Returns:
            dict[str, str]: Extracted values keyed by placeholder names
            
        Raises:
            ValueError: If the resource has invalid format
        """
    
    @abstractmethod
    def load_entity(self, entity_id: str) -> dict[str, any]:
        """
        Load entity data from AWS based on the provided identifier.
        
        Args:
            entity_id (str): The identifier of the entity to load
            
        Returns:
            dict[str, any]: The loaded entity data
        """
    
    
    @abstractmethod
    def get_additional_config(self) -> dict[str, Any]:
        """
        Additional boto3 configuration for AWS entity
        
        Returns:
            dict[str, Any]: Additional boto3 configuration
        """
    
    @abstractmethod
    def _supported_metrics(self) -> list[str]:
        """
        List of supported metric names. If empty, any metric name is supported.
        
        Returns:
            list[str]: List of supported metric names or an empty list if any value is allowed.
        """
    
    
    def validate_alarm(self, validator: AwsAlarmValidator) -> dict[str, any]:
        """
        Validates a complete CloudWatch alarm configuration.
        
        Args:
            validator (AwsAlarmValidator): The validator instance with configuration
        """
        validated_config = {
            "metric-name":          validator.validate_metric_name(allowed=self._supported_metrics()),
            "alarm-name":           validator.validate_alarm_name(),
            "statistic":            validator.validate_statistic(),
            "period":               validator.validate_period(),
            "comparison-operator":  validator.validate_comparison_operator(),
            "threshold":            validator.validate_threshold(min_value=0.0),
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
        
        if "namespace" in validator.config:
            validated_config["namespace"] = validator.validate_namespace()
        
        if "dimensions" in validator.config:
            validated_config["dimensions"] = validator.validate_dimensions()
        
        return validated_config
    
    def to_boto3_alarm(self, alarm_config: dict[str, any]) -> dict[str, any]:
        """
        Convert the config alarm loaded from a file into a boto3 arguments list.
        
        Args:
            alarm_config (dict[str, any]): The alarm configuration

        Returns:
            dict[str, any]: The boto3 alarm configuration
        """
        cloudwatch_config = {
            "AlarmName": alarm_config["alarm-name"],
            "ComparisonOperator": alarm_config["comparison-operator"],
            "EvaluationPeriods": alarm_config["evaluation-periods"],
            "MetricName": alarm_config["metric-name"],
            "Period": alarm_config["period"],
            "Statistic": alarm_config["statistic"],
            "Threshold": alarm_config["threshold"] * 100,
            "ActionsEnabled": False
        }
        
        if "namespace" in alarm_config:
            cloudwatch_config["Namespace"] = alarm_config["namespace"]

        if "alarm-actions" in alarm_config:
            cloudwatch_config["ActionsEnabled"] = True
            cloudwatch_config["AlarmActions"] = alarm_config["alarm-actions"]

        if "treat-missing-data" in alarm_config:
            cloudwatch_config["TreatMissingData"] = alarm_config["treat-missing-data"]

        if "unit" in alarm_config:
            cloudwatch_config["Unit"] = alarm_config["unit"]

        if "tags" in alarm_config:
            cloudwatch_config["Tags"] = self.__key_value_to_aws_tuples(
                alarm_config["tags"], "Key", "Value")
        
        if "dimensions" in alarm_config:
            cloudwatch_config["Dimensions"] = self.__key_value_to_aws_tuples(
                alarm_config["dimensions"], "Name", "Value")
        
        return cloudwatch_config


    def __key_value_to_aws_tuples(self, what: dict[str, str], key_name: str, value_name: str) -> list[dict[str, str]]:
        """
        Convert dict listings into the AWS format that expects an
        array of [key: ..., value: ...] elements (or similar).
        
        Args:
            what (dict[str, str]): The dictionary listings
            key_name (str): The name of the property where key should be stored
            value_name (str): The name of the property where value should be stored

        Returns:
            list(dict[str, str]):
                The list of AWS keys and AWS values formated as [{key: ..., value: ...}, ....] for each
                key/value pair from `what`.
        """
        return [{key_name: key, value_name: value} for key, value in what]
