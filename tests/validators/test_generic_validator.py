import pytest
from typing import Dict, Any, List

from alertalot.validators.generic_validator import (
    validate_comparison_operator,
    validate_statistic,
    validate_period,
    validate_evaluation_periods,
    validate_treat_missing_data,
    validate_tags,
    validate_metric_name,
    validate_alarm_name,
    validate_threshold,
    validate_byte_size,
    validate_unit,
    validate_required_keys,
    validate_unknown_keys,
    validate_alarms_list,
    validate_alarm_entry_type,
    VALID_COMPARISON_OPERATORS,
    VALID_STATISTICS,
    VALID_MISSING_DATA_TREATMENTS,
    VALID_UNITS
)


def test__validate_comparison_operator__valid_operators():
    issues = []
    result = validate_comparison_operator({"comparison-operator": "GreaterThanOrEqualToThreshold"}, issues)
    
    assert result == "GreaterThanOrEqualToThreshold"
    assert len(issues) == 0


def test__validate_comparison_operator__invalid_operator():
    issues = []
    result = validate_comparison_operator({"comparison-operator": "InvalidOperator"}, issues)
    
    assert result == "InvalidOperator"
    assert len(issues) == 1
    assert "<at 'comparison-operator'>" in issues[0]


def test__validate_comparison_operator__custom_key():
    issues = []
    custom_key = "custom-operator"
    operator = VALID_COMPARISON_OPERATORS[0]
    alarm_config = {custom_key: operator}
    
    result = validate_comparison_operator(alarm_config, issues, key=custom_key)
    
    assert result == operator
    assert len(issues) == 0


def test__validate_comparison_operator__custom_key_invalid_operator():
    issues = []
    custom_key = "custom-operator"
    invalid_operator = "InvalidOperator"
    alarm_config = {custom_key: invalid_operator}
    
    result = validate_comparison_operator(alarm_config, issues, key=custom_key)
    
    assert result == invalid_operator
    assert len(issues) == 1
    assert f"<at '{custom_key}'> Invalid comparison operator: '{invalid_operator}'." in issues


def test__validate_statistic__valid_statistic():
    issues = []
    valid_statistic = "Average"
    result = validate_statistic({"statistic": valid_statistic}, issues)
    
    assert result == valid_statistic
    assert len(issues) == 0


def test__validate_statistic__invalid_statistic():
    issues = []
    invalid_statistic = "InvalidStatistic"
    result = validate_statistic({"statistic": invalid_statistic}, issues)
    
    assert result == invalid_statistic
    assert len(issues) == 1
    assert f"<at 'statistic'> Invalid statistic: '{invalid_statistic}'." in issues


def test__validate_statistic__custom_key():
    issues = []
    custom_key = "custom-statistic"
    valid_statistic = VALID_STATISTICS[0]
    alarm_config = {custom_key: valid_statistic}
    
    result = validate_statistic(alarm_config, issues, key=custom_key)
    
    assert result == valid_statistic
    assert len(issues) == 0


def test__validate_period__valid_period():
    issues = []
    result = validate_period({"period": "60s"}, issues)
    
    assert result == 60
    assert len(issues) == 0


def test__validate_period__less_than_minimum():
    issues = []
    result = validate_period({"period": "30s"}, issues)
    
    assert result == 30
    assert len(issues) == 1
    assert "<at 'period'>" in issues[0]


def test__validate_period__not_multiple_of_60():
    issues = []
    result = validate_period({"period": "90s"}, issues)
    
    assert result == 90
    assert len(issues) == 1
    assert "<at 'period'>" in issues[0]


def test__validate_period__custom_key():
    issues = []
    custom_key = "custom-period"
    period = "300s"
    alarm_config = {custom_key: period}
    
    result = validate_period(alarm_config, issues, key=custom_key)
    
    assert result == 300
    assert len(issues) == 0


def test__validate_evaluation_periods__valid_periods():
    issues = []
    result = validate_evaluation_periods({"evaluation-periods": "5"}, issues)
    
    assert result == 5 * 60
    assert len(issues) == 0


def test__validate_evaluation_periods__zero_value():
    issues = []
    result = validate_evaluation_periods({"evaluation-periods": "0"}, issues)
    
    assert result == 0
    assert len(issues) == 1
    assert "<at 'evaluation-periods'> Evaluation periods must be positive" in issues[0]


def test__validate_evaluation_periods__negative_value():
    issues = []
    result = validate_evaluation_periods({"evaluation-periods": "-3"}, issues)
    
    assert result == -3 * 60
    assert len(issues) == 1
    assert "<at 'evaluation-periods'> Evaluation periods must be positive" in issues[0]


def test__validate_evaluation_periods__invalid_value():
    issues = []
    result = validate_evaluation_periods({"evaluation-periods": "abc"}, issues)
    
    assert result == 0
    assert len(issues) == 1
    assert "<at 'evaluation-periods'> Invalid evaluation periods: 'abc'" in issues[0]


def test__validate_treat_missing_data__valid_value():
    issues = []
    for value in VALID_MISSING_DATA_TREATMENTS:
        issues.clear()
        result = validate_treat_missing_data({"treat-missing-data": value}, issues)
        
        assert result == value
        assert len(issues) == 0


def test__validate_treat_missing_data__invalid_value():
    issues = []
    invalid_value = "invalid-treatment"
    result = validate_treat_missing_data({"treat-missing-data": invalid_value}, issues)
    
    assert result == invalid_value
    assert len(issues) == 1
    assert f"<at 'treat-missing-data'> Invalid treat-missing-data value: '{invalid_value}'." in issues[0]


def test__validate_tags__valid_tags():
    issues = []
    tags = {"Name": "TestAlarm", "Environment": "Test"}
    result = validate_tags({"tags": tags}, issues)
    
    assert result == tags
    assert len(issues) == 0


def test__validate_tags__non_dict_tags():
    issues = []
    invalid_tags = ["tag1", "tag2"]
    result = validate_tags({"tags": invalid_tags}, issues)
    
    assert result == {}
    assert len(issues) == 1
    assert "<at 'tags'> Tags must be a dictionary" in issues[0]


def test__validate_tags__non_string_key():
    issues = []
    invalid_tags = {123: "value", "valid": "value"}
    result = validate_tags({"tags": invalid_tags}, issues)
    
    assert "valid" in result
    assert 123 not in result
    assert len(issues) == 1
    assert "<at 'tags'> Tag key must be a string" in issues[0]


def test__validate_tags__key_too_long():
    issues = []
    long_key = "a" * 129
    tags = {long_key: "value", "valid": "value"}
    result = validate_tags({"tags": tags}, issues)
    
    assert "valid" in result
    assert long_key in result
    assert len(issues) == 1
    assert "<at 'tags'> Tag key must be max 128 characters" in issues[0]


def test__validate_tags__non_string_value_converted():
    issues = []
    tags = {"key1": 123, "key2": True}
    result = validate_tags({"tags": tags}, issues)
    
    assert result["key1"] == "123"
    assert result["key2"] == "True"
    assert len(issues) == 0


def test__validate_metric_name__valid_name():
    issues = []
    metric_name = "TestMetric"
    result = validate_metric_name({"metric-name": metric_name}, issues)
    
    assert result == metric_name
    assert len(issues) == 0


def test__validate_metric_name__empty_name():
    issues = []
    result = validate_metric_name({"metric-name": ""}, issues)
    
    assert result == ""
    assert len(issues) == 1
    assert "<at 'metric-name'> Metric name must be a non-empty string" in issues[0]


def test__validate_metric_name__non_string_name():
    issues = []
    result = validate_metric_name({"metric-name": 123}, issues)
    
    assert result == 123
    assert len(issues) == 1
    assert "<at 'metric-name'> Metric name must be a non-empty string" in issues[0]


def test__validate_alarm_name__valid_name():
    issues = []
    alarm_name = "TestAlarm"
    result = validate_alarm_name({"alarm-name": alarm_name}, issues)
    
    assert result == alarm_name
    assert len(issues) == 0


def test__validate_alarm_name__empty_name():
    issues = []
    result = validate_alarm_name({"alarm-name": ""}, issues)
    
    assert result == ""
    assert len(issues) == 1
    assert "<at 'alarm-name'> Alarm name must be a non-empty string" in issues[0]


def test__validate_alarm_name__non_string_name():
    issues = []
    result = validate_alarm_name({"alarm-name": 123}, issues)
    
    assert result == 123
    assert len(issues) == 1
    assert "<at 'alarm-name'> Alarm name must be a non-empty string" in issues[0]


def test__validate_threshold__valid_threshold():
    issues = []
    threshold = 0.905
    result = validate_threshold({"threshold": threshold}, issues)
    
    assert 0.905 == float(threshold)
    assert len(issues) == 0


def test__validate_threshold__percentage_string():
    issues = []
    result = validate_threshold({"threshold": "80%"}, issues)
    
    assert result == 0.8
    assert len(issues) == 0


def test__validate_threshold__below_min_value():
    issues = []
    threshold = 0.05
    min_value = 0.10
    result = validate_threshold({"threshold": threshold}, issues, min_value=min_value)
    
    assert result == float(threshold)
    assert len(issues) == 1
    assert f"<at 'threshold'> Threshold must be at least {min_value}" in issues[0]


def test__validate_threshold__above_max_value():
    issues = []
    threshold = 0.95
    max_value = 0.90
    result = validate_threshold({"threshold": threshold}, issues, max_value=max_value)
    
    assert result == float(threshold)
    assert len(issues) == 1
    assert f"<at 'threshold'> Threshold must be at most {max_value}" in issues[0]


def test__validate_threshold__invalid_value():
    issues = []
    result = validate_threshold({"threshold": "invalid"}, issues)
    
    assert result == 0.0
    assert len(issues) == 1
    assert "<at 'threshold'> Error validating threshold" in issues[0]


def test__validate_byte_size__valid_size():
    issues = []
    result = validate_byte_size({"size": "10MB"}, issues)
    
    assert result == 10 * 1024 * 1024
    assert len(issues) == 0


def test__validate_byte_size__invalid_size():
    issues = []
    result = validate_byte_size({"size": "invalid"}, issues)
    
    assert result == 0
    assert len(issues) == 1
    assert "<at 'size'> Error validating byte size" in issues[0]


def test__validate_byte_size__custom_key():
    issues = []
    custom_key = "custom-size"
    size = "5GB"
    result = validate_byte_size({custom_key: size}, issues, key=custom_key)
    
    assert result == 5 * 1024 * 1024 * 1024
    assert len(issues) == 0


def test__validate_unit__valid_unit():
    issues = []
    for unit in VALID_UNITS:
        issues.clear()
        result = validate_unit({"unit": unit}, issues)
        
        assert result == unit
        assert len(issues) == 0


def test__validate_unit__invalid_unit():
    issues = []
    invalid_unit = "InvalidUnit"
    result = validate_unit({"unit": invalid_unit}, issues)
    
    assert result == invalid_unit
    assert len(issues) == 1
    assert f"<at 'unit'> Invalid unit: '{invalid_unit}'." in issues[0]


def test__validate_required_keys__all_present():
    issues = []
    config = {"key1": "value1", "key2": "value2", "key3": "value3"}
    required_keys = ["key1", "key2"]
    
    validate_required_keys(config, required_keys, issues)
    
    assert len(issues) == 0


def test__validate_required_keys__missing_keys():
    issues = []
    config = {"key1": "value1", "key3": "value3"}
    required_keys = ["key1", "key2", "key4"]
    
    validate_required_keys(config, required_keys, issues)
    
    assert len(issues) == 2
    assert "Missing required key 'key2'" in issues[0]
    assert "Missing required key 'key4'" in issues[1]


def test__validate_unknown_keys__no_unknown_keys():
    issues = []
    config = {"key1": "value1", "key2": "value2"}
    required_keys = ["key1"]
    optional_keys = ["key2", "key3"]
    
    validate_unknown_keys(config, required_keys, optional_keys, issues)
    
    assert len(issues) == 0


def test__validate_unknown_keys__with_unknown_keys():
    issues = []
    config = {"key1": "value1", "key2": "value2", "unknown1": "value", "unknown2": "value"}
    required_keys = ["key1"]
    optional_keys = ["key2", "key3"]
    
    validate_unknown_keys(config, required_keys, optional_keys, issues)
    
    assert len(issues) == 2
    assert "Unknown key 'unknown1'" in issues[0]
    assert "Unknown key 'unknown2'" in issues[1]


def test__validate_alarms_list__valid_list():
    issues = []
    alarms = [{"alarm1": {}}, {"alarm2": {}}]
    config = {"alarms": alarms}
    
    result = validate_alarms_list(config, issues)
    
    assert result == alarms
    assert len(issues) == 0


def test__validate_alarms_list__missing_key():
    issues = []
    config = {"something_else": []}
    
    result = validate_alarms_list(config, issues)
    
    assert result == []
    assert len(issues) == 1
    assert "Missing 'alarms' key in configuration" in issues[0]


def test__validate_alarms_list__not_a_list():
    issues = []
    config = {"alarms": {"alarm1": {}}}
    
    result = validate_alarms_list(config, issues)
    
    assert result == []
    assert len(issues) == 1
    assert "Alarms configuration must be a list" in issues[0]


def test__validate_alarm_entry_type__valid_entry():
    issues = []
    alarm_entry = {"alarm1": {"key": "value"}}
    
    result = validate_alarm_entry_type(alarm_entry, 0, issues)
    
    assert result is True
    assert len(issues) == 0


def test__validate_alarm_entry_type__not_a_dict():
    issues = []
    alarm_entry = "not a dict"
    
    result = validate_alarm_entry_type(alarm_entry, 5, issues)
    
    assert result is False
    assert len(issues) == 1
    assert "Alarm entry at index 5 must be a dictionary" in issues[0]


def test__validate_alarm_entry_type__too_many_keys():
    issues = []
    alarm_entry = {"alarm1": {}, "alarm2": {}}
    
    result = validate_alarm_entry_type(alarm_entry, 2, issues)
    
    assert result is False
    assert len(issues) == 1
    assert "Alarm entry at index 2 must have exactly one key" in issues[0]
