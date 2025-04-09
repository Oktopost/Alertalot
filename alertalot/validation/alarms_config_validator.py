from typing import Any

from alertalot.generic.parameters import Parameters
from alertalot.entities.base_aws_entity import BaseAwsEntity
from alertalot.validation.aws_alarm_validator import AwsAlarmValidator


class AlarmsConfigValidator:
    """
    Validates alarm configurations against entity requirements and parameters.
    
    This class validates that alarm configurations follow the required structure and contain
    all required keys specific to the entity type. It also handles parameter substitution
    and creates validated alarm configurations.
    """
    
    def __init__(
            self,
            entity: BaseAwsEntity,
            parameters: Parameters,
            config: dict[str, Any] | Any) -> None:
        """
        Initialize the alarms configuration validator.
        
        Args:
            entity (BaseAwsEntity): The AWS entity that will be used to validate entity-specific alarm configurations
            parameters (Parameters): Parameters object used for variable substitution in alarm configurations
            config (dict[str, Any] | Any): The raw alarm configuration to validate
        """
        self._entity = entity
        self._parameters = parameters
        self._config = config
        self._parsed_config = None
        self._issues = []
    
    
    @property
    def has_issues(self) -> bool:
        """
        Check if any issues found.
        
        Returns:
            bool: True if any issues found.
        """
        return bool(self._issues)
    
    @property
    def issues(self) -> list[str]:
        """
        List of issues found by the validate method.
        
        Returns:
            The list of issues found.
        """
        return self._issues
    
    @property
    def parsed_config(self) -> dict[str, Any] | None:
        """
        The parsed and validated configuration data with values substituted by values from the Parameters object
        if one is provided.
        
        Returns:
            dict[str, Any]: Parsed and valid config
            None: if the validation failed or not called.
        """
        return self._parsed_config
    
    
    def validate(self) -> bool:
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
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        self._parsed_config = None
        self._issues = []
        
        self.__validate_alarms_list()
        
        if self.has_issues:
            return False
        
        alarms = self._config['alarms']
        parsed_config = []
        
        for i, alarm_config in enumerate(alarms):
            if not self.__validate_alarm_entry_type(alarm_config, i):
                continue
            
            parsed_alarm_config = {}
            
            validator = AwsAlarmValidator(alarm_config, self._parameters)
            
            validator.validate_required_keys(self._entity.get_required_alarm_keys())
            validator.validate_unknown_keys(
                self._entity.get_required_alarm_keys(),
                self._entity.get_optional_alarm_keys())
            
            if not validator.issues_found:
                parsed_alarm_config = self._entity.validate_alarm(validator)
            
            if validator.issues_found:
                for issue in validator.issues:
                    self._issues.append(f"[\"alarms\"][{i}]{issue}")
            else:
                parsed_config.append(parsed_alarm_config)
            
        if not self.has_issues:
            self._parsed_config = parsed_config
        
        return not self.has_issues
    
    
    def __validate_alarms_list(self):
        """
        Validates the alarms list top level object types.
        """
        if "alarms" not in self._config:
            self._issues.append("Missing 'alarms' key in configuration")
            return
        
        alarms_list = self._config["alarms"]
        
        if not isinstance(alarms_list, list):
            self._issues.append(f"Alarms configuration must be a list, got {type(alarms_list).__name__}")
    
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
            self._issues.append(f"Alarm entry at index {index} must be a dictionary, got {type(alarm_entry).__name__}")
            return False
        
        return True
