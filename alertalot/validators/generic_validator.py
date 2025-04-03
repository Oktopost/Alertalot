from typing import Any, Dict, Optional, List

from alertalot.generic.input_parser import (
    percentage,
    str2time,
    str2bytes
)


VALID_COMPARISON_OPERATORS = [
    "GreaterThanOrEqualToThreshold",
    "GreaterThanThreshold",
    "LessThanThreshold",
    "LessThanOrEqualToThreshold",
    "LessThanLowerOrGreaterThanUpperThreshold",
    "LessThanLowerThreshold",
    "GreaterThanUpperThreshold"
]

VALID_STATISTICS = [
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

VALID_MISSING_DATA_TREATMENTS = [
    "breaching",
    "notBreaching",
    "ignore",
    "missing"
]

VALID_UNITS = [
    "Seconds", "Microseconds", "Milliseconds",
    "Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes",
    "Bits", "Kilobits", "Megabits", "Gigabits", "Terabits",
    "Percent", "Count", "Bytes/Second", "Kilobytes/Second",
    "Megabytes/Second", "Gigabytes/Second", "Terabytes/Second",
    "Bits/Second", "Kilobits/Second", "Megabits/Second",
    "Gigabits/Second", "Terabits/Second", "Count/Second", "None"
]


def validate_comparison_operator(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "comparison-operator") -> Any:
    """
    Validates that the comparison operator is one of the allowed values.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "comparison-operator".
        
    Returns:
        str: The validated comparison operator
    """
    operator = alarm_config[key]
    
    if operator not in VALID_COMPARISON_OPERATORS:
        issues.append(f"<at '{key}'> Invalid comparison operator: '{operator}'.")
    
    return operator


def validate_statistic(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "statistic") -> Any:
    """
    Validates that the statistic is one of the allowed values.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "statistic".
        
    Returns:
        str: The validated statistic
    """
    statistic = alarm_config[key]
    
    if statistic not in VALID_STATISTICS:
        issues.append(f"<at '{key}'> Invalid statistic: '{statistic}'.")
    
    return statistic


def validate_period(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "period") -> Any:
    """
    Validates and converts a period string to seconds.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "period".
        
    Returns:
        int: The period in seconds
    """
    period = alarm_config[key]
    seconds = str2time(period)
    
    if seconds < 60:
        issues.append(f"<at '{key}'> Period must be at least 60 seconds, got {seconds}")
    elif seconds % 60 != 0:
        issues.append(f"<at '{key}'> Period must be a multiple of 60 seconds, got {seconds}")
    
    return seconds


def validate_evaluation_periods(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "evaluation-periods") -> int:
    """
    Validates the evaluation periods value.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "evaluation-periods".
        
    Returns:
        int: The number of evaluation periods
    """
    periods = alarm_config[key]
    
    try:
        int_value = str2time(periods)
        
        if int_value <= 0:
            issues.append(f"<at '{key}'> Evaluation periods must be positive, got {int_value}")
        
        return int_value
    
    except ValueError as e:
        issues.append(f"<at '{key}'> Invalid evaluation periods: '{periods}'. {str(e)}.")
        
        return 0


def validate_treat_missing_data(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "treat-missing-data") -> str:
    """
    Validates the treat-missing-data option.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "treat-missing-data".
        
    Returns:
        str: The validated treat-missing-data value
    """
    value = alarm_config[key]
    
    if value not in VALID_MISSING_DATA_TREATMENTS:
        issues.append(f"<at '{key}'> Invalid treat-missing-data value: '{value}'.")
    
    return value


def validate_tags(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "tags") -> Dict[str, str]:
    """
    Validates alarm tags.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "tags".
        
    Returns:
        Dict[str, str]: Validated tags dictionary
    """
    tags = alarm_config[key]
    
    if not isinstance(tags, dict):
        issues.append(f"<at '{key}'> Tags must be a dictionary, got {type(tags).__name__}")
        return {}
    
    validated_tags = {}
    
    for tag_key, value in tags.items():
        if not isinstance(tag_key, str):
            issues.append(f"<at '{key}'> Tag key must be a string, got '{tag_key}'")
            continue
            
        if len(tag_key) > 128:
            issues.append(f"<at '{key}'> Tag key must be max 128 characters, got {len(tag_key)} characters")
        
        validated_tags[tag_key] = str(value)
    
    return validated_tags


def validate_metric_name(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "metric-name") -> str:
    """
    Validates a CloudWatch metric name.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "metric-name".
        
    Returns:
        str: The validated metric name
    """
    metric_name = alarm_config[key]
    
    if not metric_name or not isinstance(metric_name, str):
        issues.append(f"<at '{key}'> Metric name must be a non-empty string, got '{metric_name}'")
    elif len(metric_name.encode('utf-8')) > 255:
        issues.append(f"<at '{key}'> Metric name exceeds maximum length of 255 bytes: '{metric_name}'")
    
    return metric_name


def validate_alarm_name(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "alarm-name") -> str:
    """
    Validates a CloudWatch alarm name.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "alarm-name".
        
    Returns:
        str: The validated alarm name
    """
    alarm_name = alarm_config[key]
    
    if not alarm_name or not isinstance(alarm_name, str):
        issues.append(f"<at '{key}'> Alarm name must be a non-empty string, got '{alarm_name}'")
    elif len(alarm_name.encode('utf-8')) > 255:
        issues.append(f"<at '{key}'> Alarm name exceeds maximum length of 255 bytes: '{alarm_name}'")
    
    return alarm_name


def validate_threshold(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "threshold",
        min_value: Optional[float] = None,
        max_value: Optional[float] = None) -> float:
    """
    Validates a numeric threshold value within specified bounds.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "threshold".
        min_value (Optional[float], optional): Minimum allowed value (inclusive). Defaults to None.
        max_value (Optional[float], optional): Maximum allowed value (inclusive). Defaults to None.
        
    Returns:
        float: The validated threshold value
    """
    threshold_value = alarm_config[key]
    
    try:
        threshold = percentage(threshold_value)
    except ValueError as e:
        issues.append(f"<at '{key}'> Error validating threshold: {str(e)}")
        return 0.0
    
    if not isinstance(threshold, (int, float)):
        issues.append(f"<at '{key}'> Threshold must be a number, got {type(threshold).__name__}")
    else:
        if min_value is not None and threshold < min_value:
            issues.append(f"<at '{key}'> Threshold must be at least {min_value}, got {threshold}")
        
        if max_value is not None and threshold > max_value:
            issues.append(f"<at '{key}'> Threshold must be at most {max_value}, got {threshold}")
        
    return float(threshold)


def validate_byte_size(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "size") -> int:
    """
    Validates and converts a byte size string to bytes.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "size".
        
    Returns:
        int: Size in bytes
    """
    size = alarm_config[key]
    
    try:
        return str2bytes(size)
    except ValueError as e:
        issues.append(f"<at '{key}'> Error validating byte size: {str(e)}")
        return 0


def validate_unit(
        alarm_config: Dict[str, Any],
        issues: List[str],
        key: str = "unit") -> str:
    """
    Validates that the unit is a valid CloudWatch metric unit.
    
    Args:
        alarm_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        key (str, optional): The key in the config dictionary. Defaults to "unit".
        
    Returns:
        str: The validated unit
    """
    unit = alarm_config[key]
    
    if unit not in VALID_UNITS:
        issues.append(f"<at '{key}'> Invalid unit: '{unit}'.")
    
    return unit


def validate_required_keys(
        config: Dict[str, Any],
        key_list: List[str],
        issues_list: List[str]) -> None:
    """
    Validates that all required keys are present in the configuration.
    Collect issues in the provided list instead of raising exceptions.
    
    Args:
        config (Dict[str, Any]): The configuration dictionary
        key_list (List[str]): List of required keys
        issues_list (List[str]): List to collect validation issues
    """
    for key in key_list:
        if key not in config:
            issues_list.append(f"Missing required key '{key}' in alarm configuration.")


def validate_unknown_keys(
        config: Dict[str, Any],
        required_keys: List[str],
        optional_keys: List[str],
        issues_list: List[str]) -> None:
    """
    Validates that there are no unknown keys in the configuration.
    Collect issues in the provided list instead of raising exceptions.
    
    Args:
        config (Dict[str, Any]): The configuration dictionary
        required_keys (List[str]): List of required keys
        optional_keys (List[str]): List of optional keys
        issues_list (List[str]): List to collect validation issues
    """
    allowed_keys = required_keys + optional_keys
    
    for key in config:
        if key not in allowed_keys:
            issues_list.append(f"Unknown key '{key}' in EC2 alarm configuration")


def validate_alarms_list(alarms_config: Dict[str, Any], issues: List[str]) -> List:
    """
    Validates and extracts the alarms list from the configuration.
    
    Args:
        alarms_config (Dict[str, Any]): Dictionary containing the alarm configuration
        issues (List[str]): List to collect validation issues
        
    Returns:
        List: The validated list of alarms from the configuration
    """
    if "alarms" not in alarms_config:
        issues.append("Missing 'alarms' key in configuration")
        return []
    
    alarms_list = alarms_config["alarms"]
    
    if not isinstance(alarms_list, list):
        issues.append(f"Alarms configuration must be a list, got {type(alarms_list).__name__}")
        return []

    return alarms_list


def validate_alarm_entry_type(alarm_entry: Any, index: int, issues: List[str]) -> bool:
    """
    Validates that an alarm entry has the correct type and structure.
    
    Args:
        alarm_entry (Any): The alarm entry to validate
        index (int): The index of this entry in the alarms list
        issues (List[str]): List to collect validation errors (modified in-place)
        
    Returns:
        bool: True if the entry is valid, False otherwise
    """
    if not isinstance(alarm_entry, dict):
        issues.append(f"Alarm entry at index {index} must be a dictionary, got {type(alarm_entry).__name__}")
        return False
    
    if len(alarm_entry) != 1:
        issues.append(f"Alarm entry at index {index} must have exactly one key, got {len(alarm_entry)}")
        return False
    
    return True
