from abc import ABC, abstractmethod
from decimal import InvalidOperation
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
            entity_type: TargetType.EC2,
            entity_id: str | None = None):
        """
        Creates a new AWS entity instance.
        
        Args:
            entity_type (TargetType): The type of entity.
            entity_id (str | None): The ID of the entity or None if a generic Entity is created.
        """
        
        self.__entity_id = entity_id
        self.__entity_type = entity_type
    
    
    @property
    def has_entity_id(self) -> bool:
        """
        Was the object initialized with the entity ID?
        
        Returns:
            bool: True, if object initialized with the entity ID
        """
        return self.__entity_id is not None
    
    @property
    def entity_id(self) -> str | None:
        """
        Get the entity ID that this object was initialized with, if any.
        
        Returns:
            str: entity ID
            None: If object initialized without an ID
        """
        return self.__entity_id
    
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
    def _load_entity(self, entity_id: str) -> dict[str, any]:
        """
        Load entity data from AWS based on the provided identifier.
        
        Args:
            entity_id (str): The identifier of the entity to load
            
        Returns:
            dict[str, any]: The loaded entity data
        """
    
    @abstractmethod
    def _get_additional_boto3_config(self) -> dict[str, Any]:
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
    
    
    def require_entity_id(self) -> None:
        """
        Raises an exception if the entity ID is not set.
        """
        if self.entity_id is None:
            raise InvalidOperation('Entity ID must be set for for this operation')
        
    def load(self) -> dict[str, any]:
        """
        Load the entity using the entity ID this object was initialized with.
        
        Returns:
            dict[str, any]: The loaded entity data
        """
        if not self.has_entity_id:
            raise InvalidOperation("Can not load entity, no entity ID provided")
        
        return self._load_entity(self.entity_id)
    
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
    
    def get_required_alarm_keys(self) -> list[str]:
        """
        Get the list of required keys for alarms.
        
        Returns:
            list[str]: List of required alarm keys
        """
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
        """
        Get the list of optional keys for alarms.
        
        Returns:
            list[str]: List of optional alarm keys
        """
        return [
            "alarm-actions",
            "tags",
            "treat-missing-data",
            "unit",
        ]
    
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
