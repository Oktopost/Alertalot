from typing import Dict, Any, List

from alertalot.validators.generic_validator import (
    validate_alarm_name,
    validate_comparison_operator,
    validate_evaluation_periods,
    validate_metric_name,
    validate_period,
    validate_statistic,
    validate_tags,
    validate_threshold,
    validate_treat_missing_data,
    validate_unit,
    validate_unknown_keys,
    validate_required_keys,
    validate_alarms_list,
    validate_alarm_entry_type
)


EC2_VALID_METRICS = [
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

EC2_METRIC_SHORTCUTS = {
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

REQUIRED_ALARM_KEYS = [
    "metric-name",
    "alarm-name",
    "statistic",
    "period",
    "comparison-operator",
    "threshold",
    "evaluation-periods"
]

OPTIONAL_ALARM_KEYS = [
    "tags",
    "treat-missing-data",
    "unit"
]


def expand_ec2_metric_shortcut(alarm_name: str) -> str:
    """
    Expands a metric shortcut to its full name if applicable.
    
    Args:
        alarm_name (str): The alarm name potentially containing a shortcut
        
    Returns:
        str: The expanded metric name or the original if no shortcut found
    """
    if alarm_name in EC2_METRIC_SHORTCUTS:
        return EC2_METRIC_SHORTCUTS[alarm_name]
    
    return alarm_name


def validate_ec2_alarm_config(config: Dict[str, Any], issues: List[str]) -> Dict[str, Any]:
    """
    Validates a complete EC2 CloudWatch alarm configuration.
    
    Args:
        config (Dict[str, Any]): The alarm configuration dictionary
        issues (List[str]): List to collect validation issues
        
    Returns:
        Dict[str, Any]: The validated configuration with converted values
    """
    validate_required_keys(config, REQUIRED_ALARM_KEYS, issues)
    validate_unknown_keys(config, REQUIRED_ALARM_KEYS, OPTIONAL_ALARM_KEYS, issues)
    
    if issues:
        return {}
    
    validated_config = {
        "metric-name":          validate_metric_name(config, issues),
        "alarm-name":           validate_alarm_name(config, issues),
        "statistic":            validate_statistic(config, issues),
        "period":               validate_period(config, issues),
        "comparison-operator":  validate_comparison_operator(config, issues),
        "threshold":            validate_threshold(config, issues, min_value=0.0, max_value=1.0),
        "evaluation-periods":   validate_evaluation_periods(config, issues)
    }
    
    if "tags" in config:
        validated_config["tags"] = validate_tags(config, issues)
    
    if "treat-missing-data" in config:
        validated_config["treat-missing-data"] = validate_treat_missing_data(config, issues)
    
    if "unit" in config:
        validated_config["unit"] = validate_unit(config, issues)
    
    return validated_config


def validate_ec2_alarms(alarms_config: Dict[str, Any], issues: List[str]) -> Dict[str, Any]:
    """
    Validates EC2 CloudWatch alarm configurations.
    
    Args:
        alarms_config (Dict[str, Any]): Full alarms configuration
        issues (List[str]): List to collect validation errors (modified in-place)
        
    Returns:
        Dict[str, Any]: Validated alarms configuration
    """
    parsed_config = []
    alarms_list = validate_alarms_list(alarms_config, issues)
    
    for i, alarm_entry in enumerate(alarms_list):
        if not validate_alarm_entry_type(alarm_entry, i, issues):
            continue
        
        alarm_type = list(alarm_entry.keys())[0]
        alarm_config = alarm_entry[alarm_type]
        
        expanded_alarm_type = expand_ec2_metric_shortcut(alarm_type)
        
        if not isinstance(alarm_config, dict):
            issues.append(
                f"Alarm configuration for '{alarm_type}' at index {i} must be "
                f"a dictionary, got {type(alarm_config).__name__}")
            
            continue
        
        alarm_issues = []
        validated_config = validate_ec2_alarm_config(alarm_config, alarm_issues)
        parsed_config.append({expanded_alarm_type: validated_config})
        
        for issue in alarm_issues:
            issues.append(f"In alarm '{alarm_type}' at index {i}: {issue}")
    
    return {"alarms": parsed_config}
