from typing import Any

from alertalot.generic.variables import Variables
from alertalot.entities.base_aws_entity import BaseAwsEntity
from alertalot.validation.aws_alarm_validator import AwsAlarmValidator
from alertalot.entities.aws_entity_factory import AwsEntityFactory
from alertalot.generic.target_type import TargetType
from alertalot.entities.aws_generic_entity import AwsGenericEntity


class AlarmsConfigValidator:
    """
    Validates alarm configurations against entity requirements and variables.
    
    This class validates that alarm configurations follow the required structure and contain
    all required keys specific to the entity type. It also handles variables substitution
    and creates validated alarm configurations.
    """
    
    def __init__(
            self,
            variables: Variables,
            config: dict[str, Any] | Any) -> None:
        """
        Initialize the alarms configuration validator.
        
        Args:
            variables (Variables): Parameters object used for variable substitution in alarm configurations
            config (dict[str, Any] | Any): The raw alarm configuration to validate
        """
        self.__vars = variables
        self.__config = config
        self.__parsed_config = None
        self.__issues = []
    
    
    @property
    def has_issues(self) -> bool:
        """
        Check if any issues found.
        
        Returns:
            bool: True if any issues found.
        """
        return bool(self.__issues)
    
    @property
    def issues(self) -> list[str]:
        """
        List of issues found by the validate method.
        
        Returns:
            The list of issues found.
        """
        return self.__issues
    
    @property
    def parsed_config(self) -> dict[str, Any] | None:
        """
        The parsed and validated configuration data with values substituted by values from the Parameters object
        if one is provided.
        
        Returns:
            dict[str, Any]: Parsed and valid config
            None: if the validation failed or not called.
        """
        return self.__parsed_config
    
    
    def validate(self, is_strict: bool = True) -> bool:
        """
        Validates the alarm configuration and populates parsed_config with processed alarms.
        
        Performs validation in multiple stages:
        1. Validates the basic structure of the alarms configuration
        2. For each alarm entry:
           - Validates it has the correct type
           - Validates required and optional keys
           - Validates alarm-specific properties using the entity validator
        3. Collects validation issues for reporting
        
        This method is idempotent and can be called multiple times without side effects.
        After validation, any issues found are available through the `issues` property.
        
        Args:
            is_strict (bool): If False, do not fail the validation for variable substitution cases.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        self.__parsed_config = None
        self.__issues = []
        
        self.__validate_alarms_list()
        
        if self.has_issues:
            return False
        
        alarms = self.__config['alarms']
        parsed_config = []
        
        for i, alarm_config in enumerate(alarms):
            if not self.__validate_alarm_entry_type(alarm_config, i):
                continue
            
            entity = self.__validate_entity_type(alarm_config)
            
            alarm_config = alarm_config | entity.get_additional_config()
            
            validator = AwsAlarmValidator(alarm_config, self.__vars, is_preview=not is_strict)
            
            validator.validate_keys(
                AlarmsConfigValidator.__get_required_alarm_keys(),
                AlarmsConfigValidator.__get_optional_alarm_keys())
            
            if not validator.issues_found:
                parsed_alarm_config = (
                    {"type": self.__get_type(alarm_config)} |
                    entity.validate_alarm(validator))
            
                if not validator.issues_found:
                    parsed_config.append(parsed_alarm_config)
            
            if validator.issues_found:
                for issue in validator.issues:
                    if len(issue) > 0 and issue[0] != '[':
                        issue = ' ' + issue
                    
                    self.__issues.append(f"[\"alarms\"][{i}]{issue}")
            
        if not self.has_issues:
            self.__parsed_config = parsed_config
        
        return not self.has_issues
    
    
    def __validate_alarms_list(self):
        """
        Validates the alarms list top level object types.
        """
        if "alarms" not in self.__config:
            self.__issues.append("Missing 'alarms' key in configuration")
            return
        
        alarms_list = self.__config["alarms"]
        
        if not isinstance(alarms_list, list):
            self.__issues.append(f"Alarms configuration must be a list, got {type(alarms_list).__name__}")
    
    def __validate_alarm_entry_type(self, alarm_entry: Any, index: int) -> bool:
        """
        Validates that an alarm entry has the correct type and structure.
        
        Args:
            alarm_entry (Any): The alarm entry to validate
            index (int): The index of this entry in the alarms list.
        
        Returns:
            bool: True if an alarm entry has the correct type and structure.
        """
        if not isinstance(alarm_entry, dict):
            self.__issues.append(f"Alarm entry at index {index} must be a dictionary, got {type(alarm_entry).__name__}")
            return False
        
        return True
    
    
    def __get_type(self, alarm_config: dict[str, Any]) -> str:
        """
        Get the type of the alarm's target entity.
        
        Args:
            alarm_config (dict[str, Any]): The alarm configuration

        Returns:
            str: The type of the alarm's target entity.
        """
        if "type" in alarm_config:
            return alarm_config["type"]
        
        return TargetType.GENERIC.value
    
    def __validate_entity_type(self, alarm_entry: dict[str, Any]) -> BaseAwsEntity:
        """
        Return the target entity type of the current alarm configuration.
        
        Args:
            alarm_entry (dict[str, Any]): The alarm entry to use.

        Returns:
            BaseAwsEntity: The entity type to use.
        """
        if "type" not in alarm_entry:
            return AwsGenericEntity()
        
        target_type = TargetType.require(alarm_entry["type"])
        
        return AwsEntityFactory.from_type(target_type)


    @staticmethod
    def __get_required_alarm_keys() -> list[str]:
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
    
    @staticmethod
    def __get_optional_alarm_keys() -> list[str]:
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
            "namespace",
            "dimensions"
        ]
