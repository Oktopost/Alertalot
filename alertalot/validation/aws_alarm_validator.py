from typing import Any, ClassVar

from alertalot.generic.input_parser import (
    percentage,
    str2time,
    str2bytes
)
from alertalot.generic.variables import Variables


class AwsAlarmValidator:
    """
    Validator for AWS CloudWatch Alarm configurations.
    """
    
    VALID_COMPARISON_OPERATORS: ClassVar[list[str]] = [
        "GreaterThanOrEqualToThreshold",
        "GreaterThanThreshold",
        "LessThanThreshold",
        "LessThanOrEqualToThreshold",
        "LessThanLowerOrGreaterThanUpperThreshold",
        "LessThanLowerThreshold",
        "GreaterThanUpperThreshold"
    ]

    VALID_STATISTICS: ClassVar[list[str]] = [
        "Average",
        "Maximum",
        "Minimum",
        "SampleCount",
        "Sum",
        "p90",
        "p95",
        "p99",
        "p99.9"
    ]

    VALID_MISSING_DATA_TREATMENTS: ClassVar[list[str]] = [
        "breaching",
        "notBreaching",
        "ignore",
        "missing"
    ]

    VALID_UNITS: ClassVar[list[str]] = [
        "Seconds", "Microseconds", "Milliseconds",
        "Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes",
        "Bits", "Kilobits", "Megabits", "Gigabits", "Terabits",
        "Percent", "Count", "Bytes/Second", "Kilobytes/Second",
        "Megabytes/Second", "Gigabytes/Second", "Terabytes/Second",
        "Bits/Second", "Kilobits/Second", "Megabits/Second",
        "Gigabits/Second", "Terabits/Second", "Count/Second", "None"
    ]
    
    
    def __init__(
            self,
            config: dict[str, Any],
            variables: Variables,
            *,
            is_preview: bool = False):
        """
        Initialize the AWS Alarm Validator.
        
        Args:
            config (dict[str, Any]): Dictionary containing the alarm configuration
            variables (Variables): Parameters to use for value resolution
            is_preview (bool):
                If set to true, the output does not need to be strictly validated and the
                variables are optional
        """
        self.__vars = variables
        self.__config = config
        self.__issues = []
        self.__is_preview = is_preview
    
    
    @property
    def config(self) -> dict[str, Any]:
        """
        Get the alarm configuration.
        
        Returns:
            dict[str, Any]: The alarm configuration
        """
        return self.__config
    
    @property
    def issues(self) -> list[str]:
        """
        Get the list of validation issues.
        
        Returns:
            list[str]: The list of validation issues
        """
        return self.__issues
    
    @property
    def issues_found(self) -> bool:
        """
        Check if any issues were found during validation.
        
        Returns:
            bool: True if any issues were found
        """
        return bool(self.__issues)
    
    
    def validate_keys(self, required_keys: list[str], optional_keys: list[str]) -> None:
        """
        Validate that all required keys are present and there are no unknown keys.
        
        Args:
            required_keys (list[str]): List of keys that must be present in the configuration
            optional_keys (list[str]): List of keys that may be present
        """
        self.validate_required_keys(required_keys)
        self.validate_unknown_keys(required_keys, optional_keys)
    
    def validate_required_keys(self, required_keys: list[str]) -> None:
        """
        Validates that all required keys are present in the configuration.
        
        Args:
            required_keys (list[str]): List of keys that must be present in the configuration
        """
        for key in required_keys:
            if key not in self.__config:
                self.__issues.append(f"Missing required key '{key}' in alarm configuration.")
    
    def validate_unknown_keys(self, required_keys: list[str], optional_keys: list[str]) -> None:
        """
        Validates that there are no unknown keys in the configuration.
        
        Args:
            required_keys (list[str]): List of keys that must be present
            optional_keys (list[str]): List of keys that may be present
        """
        for key in self.__config:
            if key == "type":
                continue
            if key not in optional_keys and key not in required_keys:
                self.__issues.append(f"Unknown key '{key}' in EC2 alarm configuration")
    
    
    def validate_comparison_operator(self) -> str:
        """
        Validates that the comparison operator is one of the allowed values.
        
        Returns:
            str: The validated comparison operator
        """
        key = "comparison-operator"
        operator = self.__config[key]
        
        if operator not in self.VALID_COMPARISON_OPERATORS:
            self.__append_issue(key, f"Invalid comparison operator: '{operator}'.")
        
        return operator

    def validate_statistic(self) -> str:
        """
        Validates that the statistic is one of the allowed values.
        
        Returns:
            str: The validated statistic
        """
        key = "statistic"
        statistic = self.__config[key]
        
        if statistic not in self.VALID_STATISTICS:
            self.__append_issue(key, f"Invalid statistic: '{statistic}'.")
        
        return statistic

    def validate_period(self, key = "period") -> int:
        """
        Validates and converts a period string to seconds.
        
        Returns:
            int: The period in seconds
        """
        key = "period"
        period = self.__config[key]
        
        try:
            seconds = str2time(period)
        except ValueError as e:
            self.__append_issue(key, f"{e}")
            return 0
        
        if seconds < 60:
            self.__append_issue(key, f"Period must be at least 60 seconds, got {seconds}")
        elif seconds % 60 != 0:
            self.__append_issue(key, f"Period must be a multiple of 60 seconds, got {seconds}")
        
        return seconds

    def validate_evaluation_periods(self) -> int:
        """
        Validates the evaluation periods value.
        
        Returns:
            int: The number of evaluation periods
        """
        key = "evaluation-periods"
        periods = self.__config[key]
        
        try:
            int_value = str2time(periods)
            
            if int_value <= 0:
                self.__append_issue(key, f"Evaluation periods must be positive, got {int_value}")
            
            return int_value
        
        except ValueError as e:
            self.__append_issue(key, f"Invalid evaluation periods: '{periods}'. {str(e)}.")
            return 0

    def validate_treat_missing_data(self) -> str:
        """
        Validates the treat-missing-data option.
        
        Returns:
            str: The validated treat-missing-data value
        """
        key = "treat-missing-data"
        value = self.__config[key]
        
        if value not in self.VALID_MISSING_DATA_TREATMENTS:
            self.__append_issue(key, f"Invalid treat-missing-data value: '{value}'.")
        
        return value

    def validate_alarm_actions(self) -> list[str]:
        """
        Validates a list of SNS topic ARNs to be used as alarm actions.
        Supports both a single string and a list of strings.
        
        Returns:
            list[str]: The validated list of SNS topic ARNs
        """
        key = "alarm-actions"
        
        if key not in self.__config:
            return []
            
        actions = self.__config[key]
        
        if isinstance(actions, str):
            actions = [actions]
        elif not isinstance(actions, list):
            self.__append_issue(key, f"Alarm actions must be a string or list, got {type(actions).__name__}")
            return []
            
        validated_actions = []
        
        for i, action in enumerate(actions):
            if not isinstance(action, str):
                self.__issues.append(f"[\"{key}\"][{i}] Action must be a string (ARN), got {type(action).__name__}")
                continue
            
            try:
                action = self.__vars.substitute(action, fail_if_missing=not self.__is_preview)
            except KeyError as e:
                self.__issues.append(f"[\"{key}\"][{i}] {e}")
            
            if not self.__is_preview and not action.startswith("arn:aws:sns:"):
                self.__issues.append(f"[\"{key}\"][{i}] Invalid SNS topic ARN format: '{action}'")
            
            validated_actions.append(action)
            
        return validated_actions

    def validate_tags(self) -> dict[str, str]:
        """
        Validates alarm tags.
        
        Returns:
            dict[str, str]: Validated tags dictionary
        """
        key = "tags"
        
        if key not in self.__config:
            return {}
        
        tags = self.__config[key]
        
        if not isinstance(tags, dict):
            self.__append_issue(key, f"Tags must be a dictionary, got {type(tags).__name__}")
            return {}
        
        validated_tags = {}
        
        for tag_key, value in tags.items():
            if not isinstance(tag_key, str):
                self.__append_issue(key, f"Tag key must be a string, got '{tag_key}'")
                continue
                
            if len(tag_key) > 128:
                self.__append_issue(key, f"Tag key must be max 128 characters, got {len(tag_key)} characters")
            
            try:
                validated_tags[tag_key] = self.__vars.substitute(value, fail_if_missing=not self.__is_preview)
            except KeyError as e:
                self.__issues.append(f"\"{key}\"] {e}")
        
        return validated_tags
    
    def validate_dimensions(self) -> dict[str, str]:
        """
        Validates alarm dimensions.
        
        Returns:
            dict[str, str]: Validated dimensions dictionary
        """
        key = "dimensions"
        
        if key not in self.__config:
            return {}
        
        tags = self.__config[key]
        
        if not isinstance(tags, dict):
            self.__append_issue(key, f"Dimensions must be a dictionary, got {type(tags).__name__}")
            return {}
        
        validated_dimension = {}
        
        for tag_key, value in tags.items():
            if not isinstance(tag_key, str):
                self.__append_issue(key, f"Dimension key must be a string, got '{tag_key}'")
                continue
                
            if len(tag_key) > 128:
                self.__append_issue(key, f"Dimension key must be max 128 characters, got {len(tag_key)}")
            
            try:
                validated_dimension[tag_key] = self.__vars.substitute(value, fail_if_missing=not self.__is_preview)
            except KeyError as e:
                self.__issues.append(f"\"{key}\"] {e}")
        
        return validated_dimension
    
    def validate_metric_name(self, allowed: list[str] | None = None) -> str:
        """
        Validates a CloudWatch metric name.
        
        Args:
            allowed (list[str] | None): Allowed metric names. If not set, any name will be accepted.
            
        Returns:
            str: The validated metric name
        """
        key = "metric-name"
        
        metric_name = self.__config[key]
        
        if not isinstance(metric_name, str):
            self.__append_issue(
                key,
                f"Metric name must be a non-empty string, got '{type(metric_name).__name__}'")
            return ""
        
        try:
            metric_name = self.__vars.substitute(metric_name, fail_if_missing=not self.__is_preview)
        except KeyError as e:
            self.__append_issue(key, f"{str(e)}")
            return metric_name
        
        if self.__is_preview:
            return metric_name
        
        if len(metric_name.encode('utf-8')) > 255:
            self.__append_issue(key, f"Metric name exceeds maximum length of 255 bytes: '{metric_name}'")
        
        if allowed is not None:
            if metric_name not in allowed:
                self.__append_issue(key, f"Metric '{metric_name}', is not a valid metric name")
        
        return metric_name

    def validate_alarm_name(self) -> str:
        """
        Validates a CloudWatch alarm name.
        
        Returns:
            str: The validated alarm name
        """
        key = "alarm-name"
        
        alarm_name = self.__config[key]
        
        if not alarm_name or not isinstance(alarm_name, str):
            self.__append_issue(key, f"Alarm name must be a non-empty string, "
                                f"got '{type(alarm_name).__name__}'")
            return ""
        
        try:
            alarm_name = self.__vars.substitute(alarm_name, fail_if_missing=not self.__is_preview)
        except KeyError as e:
            self.__append_issue(key, f"{str(e)}")
            return alarm_name
        
        if self.__is_preview:
            return alarm_name
        
        if len(alarm_name.encode('utf-8')) > 255:
            self.__append_issue(key, f"Alarm name exceeds maximum length of 255 bytes: '{alarm_name}'")
        
        return alarm_name

    def validate_threshold(
            self,
            min_value: float | None = None,
            max_value: float | None = None) -> float:
        """
        Validates a numeric threshold value within specified bounds.
        
        Args:
            min_value (float): Minimum allowed value (inclusive). Defaults to None
            max_value (float): Maximum allowed value (inclusive). Defaults to None
            
        Returns:
            float: The validated threshold value
        """
        key = "threshold"
        
        threshold_value = self.__config[key]
        
        try:
            threshold = percentage(threshold_value)
        except ValueError as e:
            self.__append_issue(key, f"Error validating threshold: {str(e)}")
            return 0.0
        
        if min_value is not None and threshold < min_value:
            self.__append_issue(key, f"Threshold must be at least {min_value}, got {threshold}")
        
        if max_value is not None and threshold > max_value:
            self.__append_issue(key, f"Threshold must be at most {max_value}, got {threshold}")
            
        return float(threshold)

    def validate_byte_size(self) -> int:
        """
        Validates and converts a byte size string to bytes.
        
        Returns:
            int: Size in bytes
        """
        key = "size"
        
        size = self.__config[key]
        
        try:
            return str2bytes(size)
        except ValueError as e:
            self.__append_issue(key, f"Error validating byte size: {str(e)}")
            return 0

    def validate_unit(self) -> str:
        """
        Validates that the unit is a valid CloudWatch metric unit.
        
        Returns:
            str: The validated unit
        """
        key = "unit"
        
        unit = self.__config[key]
        
        if unit not in self.VALID_UNITS:
            self.__append_issue(key, f"Invalid unit: '{unit}'.")
        
        return unit

    def validate_namespace(self) -> str:
        """
        Validate that namespace is a valid string.
        
        Returns:
            str: The validated namespace
        """
        namespace = self.__config["namespace"]
        
        if not isinstance(namespace, str):
            self.__issues.append(f"[\"namespace\"] Namespace must be a string.")
            return ""
        
        try:
            namespace = self.__vars.substitute(namespace, fail_if_missing=not self.__is_preview)
        except KeyError as e:
            self.__issues.append(f"[\"namespace\"] {e}")
        
        return namespace
    
    
    def __append_issue(self, key: str, message: str) -> None:
        self.__issues.append(f"[\"{key}\"] {message}")
