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
    
    
    def __init__(self, config: dict[str, Any], vars: Variables):
        """
        Initialize the AWS Alarm Validator.
        
        Args:
            config (dict[str, Any]): Dictionary containing the alarm configuration
            vars (Variables): Parameters to use for value resolution
        """
        self.__vars = vars
        self.__config = config
        self.__issues = []
    
    
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
            if key not in optional_keys and key not in required_keys:
                self.__issues.append(f"Unknown key '{key}' in EC2 alarm configuration")
    
    
    def validate_comparison_operator(self, key: str = "comparison-operator") -> str:
        """
        Validates that the comparison operator is one of the allowed values.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "comparison-operator"
            
        Returns:
            str: The validated comparison operator
        """
        operator = self.__config[key]
        
        if operator not in self.VALID_COMPARISON_OPERATORS:
            self.__issues.append(f"[\"{key}\"] Invalid comparison operator: '{operator}'.")
        
        return operator

    def validate_statistic(self, key: str = "statistic") -> str:
        """
        Validates that the statistic is one of the allowed values.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "statistic"
            
        Returns:
            str: The validated statistic
        """
        statistic = self.__config[key]
        
        if statistic not in self.VALID_STATISTICS:
            self.__issues.append(f"[\"{key}\"] Invalid statistic: '{statistic}'.")
        
        return statistic

    def validate_period(self, key: str = "period") -> int:
        """
        Validates and converts a period string to seconds.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "period"
            
        Returns:
            int: The period in seconds
        """
        period = self.__config[key]
        
        try:
            seconds = str2time(period)
        except ValueError as e:
            self.__issues.append(f"[\"{key}\"] {e}")
            return period
        
        if seconds < 60:
            self.__issues.append(f"[\"{key}\"] Period must be at least 60 seconds, got {seconds}")
        elif seconds % 60 != 0:
            self.__issues.append(f"[\"{key}\"] Period must be a multiple of 60 seconds, got {seconds}")
        
        return seconds

    def validate_evaluation_periods(self, key: str = "evaluation-periods") -> int:
        """
        Validates the evaluation periods value.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "evaluation-periods".
            
        Returns:
            int: The number of evaluation periods
        """
        periods = self.__config[key]
        
        try:
            int_value = str2time(periods)
            
            if int_value <= 0:
                self.__issues.append(f"[\"{key}\"] Evaluation periods must be positive, got {int_value}")
            
            return int_value
        
        except ValueError as e:
            self.__issues.append(f"[\"{key}\"] Invalid evaluation periods: '{periods}'. {str(e)}.")
            
            return 0

    def validate_treat_missing_data(self, key: str = "treat-missing-data") -> str:
        """
        Validates the treat-missing-data option.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "treat-missing-data".
            
        Returns:
            str: The validated treat-missing-data value
        """
        value = self.__config[key]
        
        if value not in self.VALID_MISSING_DATA_TREATMENTS:
            self.__issues.append(f"[\"{key}\"] Invalid treat-missing-data value: '{value}'.")
        
        return value

    def validate_alarm_actions(self, key: str = "alarm-actions") -> list[str]:
        """
        Validates a list of SNS topic ARNs to be used as alarm actions.
        Supports both a single string and a list of strings.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "alarm-actions".
            
        Returns:
            list[str]: The validated list of SNS topic ARNs
        """
        if key not in self.__config:
            return []
            
        actions = self.__config[key]
        
        if isinstance(actions, str):
            actions = [actions]
        elif not isinstance(actions, list):
            self.__issues.append(f"[\"{key}\"] Alarm actions must be a string or list, got {type(actions).__name__}")
            return []
            
        validated_actions = []
        
        for i, action in enumerate(actions):
            if not isinstance(action, str):
                self.__issues.append(f"[\"{key}\"][{i}] Action must be a string (ARN), got {type(action).__name__}")
                continue
            
            try:
                action = self.__vars.substitute(action)
            except KeyError as e:
                self.__issues.append(f"[\"{key}\"][{i}] {e}")
                continue
            
            if not action.startswith("arn:aws:sns:"):
                self.__issues.append(f"[\"{key}\"][{i}] Invalid SNS topic ARN format: '{action}'")
            
            validated_actions.append(action)
            
        return validated_actions

    def validate_tags(self, key: str = "tags") -> dict[str, str]:
        """
        Validates alarm tags.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "tags".
            
        Returns:
            dict[str, str]: Validated tags dictionary
        """
        if key not in self.__config:
            return {}
        
        tags = self.__config[key]
        
        if not isinstance(tags, dict):
            self.__issues.append(f"[\"{key}\"] Tags must be a dictionary, got {type(tags).__name__}")
            return {}
        
        validated_tags = {}
        
        for tag_key, value in tags.items():
            if not isinstance(tag_key, str):
                self.__issues.append(f"[\"{key}\"] Tag key must be a string, got '{tag_key}'")
                continue
                
            if len(tag_key) > 128:
                self.__issues.append(f"[\"{key}\"] Tag key must be max 128 characters, got {len(tag_key)} characters")
            
            try:
                validated_tags[tag_key] = self.__vars.substitute(value)
            except KeyError as e:
                self.__issues.append(f"\"{key}\"] {e}")
        
        return validated_tags
    
    def validate_metric_name(self, key: str = "metric-name", allowed: list[str] | None = None) -> str:
        """
        Validates a CloudWatch metric name.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "metric-name".
            allowed (list[str] | None): Allowed metric names. If not set, any name will be accepted.
            
        Returns:
            str: The validated metric name
        """
        metric_name = self.__config[key]
        
        if not isinstance(metric_name, str):
            self.__issues.append(f"[\"{key}\"] Metric name must be a non-empty string, "
                                f"got '{type(metric_name).__name__}'")
        
        metric_name = self.__expand_ec2_metric_shortcut(metric_name)
        
        try:
            metric_name = self.__vars.substitute(metric_name)
        except KeyError as e:
            self.__issues.append(f"[\"{key}\"] {str(e)}")
            return metric_name
        
        if len(metric_name.encode('utf-8')) > 255:
            self.__issues.append(f"[\"{key}\"] Metric name exceeds maximum length of 255 bytes: '{metric_name}'")
        
        if allowed is not None:
            if metric_name not in allowed:
                self.__issues.append(f"[\"{key}\"] Metric '{metric_name}', is not a valid metric name")
        
        return metric_name

    def validate_alarm_name(self, key: str = "alarm-name") -> str:
        """
        Validates a CloudWatch alarm name.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "alarm-name".
            
        Returns:
            str: The validated alarm name
        """
        alarm_name = self.__config[key]
        
        if not alarm_name or not isinstance(alarm_name, str):
            self.__issues.append(f"[\"{key}\"] Alarm name must be a non-empty string, "
                                f"got '{type(alarm_name).__name__}'")
        
        try:
            alarm_name = self.__vars.substitute(alarm_name)
        except KeyError as e:
            self.__issues.append(f"[\"{key}\"] {str(e)}")
            return alarm_name
        
        if len(alarm_name.encode('utf-8')) > 255:
            self.__issues.append(f"[\"{key}\"] Alarm name exceeds maximum length of 255 bytes: '{alarm_name}'")
        
        return alarm_name

    def validate_threshold(
            self,
            key: str = "threshold",
            min_value: float | None = None,
            max_value: float | None = None) -> float:
        """
        Validates a numeric threshold value within specified bounds.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "threshold"
            min_value (float): Minimum allowed value (inclusive). Defaults to None
            max_value (float): Maximum allowed value (inclusive). Defaults to None
            
        Returns:
            float: The validated threshold value
        """
        threshold_value = self.__config[key]
        
        try:
            threshold = percentage(threshold_value)
        except ValueError as e:
            self.__issues.append(f"[\"{key}\"] Error validating threshold: {str(e)}")
            return 0.0
        
        if not isinstance(threshold, (int, float)):
            self.__issues.append(f"[\"{key}\"] Threshold must be a number, got {type(threshold).__name__}")
        else:
            if min_value is not None and threshold < min_value:
                self.__issues.append(f"[\"{key}\"] Threshold must be at least {min_value}, got {threshold}")
            
            if max_value is not None and threshold > max_value:
                self.__issues.append(f"[\"{key}\"] Threshold must be at most {max_value}, got {threshold}")
            
        return float(threshold)

    def validate_byte_size(self, key: str = "size") -> int:
        """
        Validates and converts a byte size string to bytes.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "size".
            
        Returns:
            int: Size in bytes
        """
        size = self.__config[key]
        
        try:
            return str2bytes(size)
        except ValueError as e:
            self.__issues.append(f"[\"{key}\"] Error validating byte size: {str(e)}")
            return 0

    def validate_unit(self, key: str = "unit") -> str:
        """
        Validates that the unit is a valid CloudWatch metric unit.
        
        Args:
            key (str): The key in the config dictionary. Defaults to "unit".
            
        Returns:
            str: The validated unit
        """
        unit = self.__config[key]
        
        if unit not in self.VALID_UNITS:
            self.__issues.append(f"[\"{key}\"] Invalid unit: '{unit}'.")
        
        return unit
    
    
    def __expand_ec2_metric_shortcut(self, metric_name: str) -> str:
        """
        Check if the metric name is written in the shortcut format and if so expand it to the correct format.
        
        Args:
            metric_name (str): The metric name to expand, if necessary

        Returns:
            str: The expanded metric name or the original name if not a shortcut
        """
        shortcuts = {
            "cpu": "CPUUtilization",
            "disk-read": "DiskReadOps",
            "disk-write": "DiskWriteOps",
            "disk-read-bytes": "DiskReadBytes",
            "disk-write-bytes": "DiskWriteBytes",
            "network-in": "NetworkIn",
            "network-out": "NetworkOut",
            "network-packets-in": "NetworkPacketsIn",
            "network-packets-out": "NetworkPacketsOut",
            "status-check": "StatusCheckFailed",
            "status-check-instance": "StatusCheckFailed_Instance",
            "status-check-system": "StatusCheckFailed_System",
            "ebs-read": "EBSReadOps",
            "ebs-write": "EBSWriteOps",
            "ebs-read-bytes": "EBSReadBytes",
            "ebs-write-bytes": "EBSWriteBytes",
            "ebs-io-balance": "EBSIOBalance%",
            "ebs-byte-balance": "EBSByteBalance%"
        }
        
        if metric_name in shortcuts:
            return shortcuts[metric_name]
        
        return metric_name
