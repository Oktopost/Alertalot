from alertalot.validation.aws_alarm_validator import AwsAlarmValidator
from alertalot.generic.variables import Variables



def test__sanity():
    config = {"comparison-operator": "InvalidOperator"}
    validator = AwsAlarmValidator(config, Variables())
    
    assert config == validator.config


def test__validate_comparison_operator__valid():
    valid_operators = AwsAlarmValidator.VALID_COMPARISON_OPERATORS
    
    for operator in valid_operators:
        config = {"comparison-operator": operator}
        validator = AwsAlarmValidator(config, Variables())
        
        assert validator.validate_comparison_operator() == operator
        assert not validator.issues_found


def test__validate_comparison_operator__invalid():
    config = {"comparison-operator": "InvalidOperator"}
    validator = AwsAlarmValidator(config, Variables())
    
    validator.validate_comparison_operator()
    
    assert validator.issues_found
    assert any("Invalid" in issue for issue in validator.issues)


def test__validate_statistic__valid():
    valid_statistics = AwsAlarmValidator.VALID_STATISTICS
    
    for statistic in valid_statistics:
        config = {"statistic": statistic}
        validator = AwsAlarmValidator(config, Variables())
        
        assert validator.validate_statistic() == statistic
        assert not validator.issues_found


def test__validate_statistic__invalid():
    config = {"statistic": "InvalidStatistic"}
    validator = AwsAlarmValidator(config, Variables())
    
    validator.validate_statistic()
    
    assert validator.issues_found
    assert any("Invalid" in issue for issue in validator.issues)


def test__validate_period__valid():
    test_cases = [
        ("60s", 60),
        ("1m", 60),
        ("5m", 5 * 60),
        ("1h", 60 * 60),
        ("24h", 24 * 60 * 60)
    ]
    
    for period_str, expected_seconds in test_cases:
        config = {"period": period_str}
        validator = AwsAlarmValidator(config, Variables())
        
        assert validator.validate_period() == expected_seconds
        assert not validator.issues_found


def test__validate_period__value_substituted():
    config = {"period": "$VAL"}
    validator = AwsAlarmValidator(config, Variables({"VAL": "2 minutes"}))
    
    assert validator.validate_period() == 2 * 60
    assert not validator.issues_found


def test__validate_period__invalid():
    config = {"period": "abc"}
    validator = AwsAlarmValidator(config, Variables())
    
    assert validator.validate_period() == 0
    assert validator.issues_found


def test__validate_period__invalid_struct():
    config = {"period": ['abc']}
    validator = AwsAlarmValidator(config, Variables())
    
    assert validator.validate_period() == 0
    assert validator.issues_found


def test__validate_period__too_short():
    config = {"period": "30s"}
    validator = AwsAlarmValidator(config, Variables())
    
    validator.validate_period()
    
    assert validator.issues_found
    assert any("60" in issue for issue in validator.issues)


def test__validate_period__not_multiple_of_60():
    config = {"period": "90s"}
    validator = AwsAlarmValidator(config, Variables())
    
    validator.validate_period()
    
    assert validator.issues_found
    assert any("Period must be a multiple of 60 seconds" in issue for issue in validator.issues)


def test__validate_evaluation_periods__valid():
    test_cases = [
        ("1", 1),
        ("5", 5),
        ("10", 10)
    ]
    
    for periods_str, expected_value in test_cases:
        config = {"evaluation-periods": periods_str}
        validator = AwsAlarmValidator(config, Variables())
        
        assert validator.validate_evaluation_periods() == expected_value
        assert not validator.issues_found


def test__validate_evaluation_periods__invalid():
    config = {"evaluation-periods": "adsadas"}
    validator = AwsAlarmValidator(config, Variables())
    
    assert validator.validate_evaluation_periods() == 0
    assert validator.issues_found


def test__validate_evaluation_periods__value_substituted():
    config = {"evaluation-periods": "$VAL"}
    validator = AwsAlarmValidator(config, Variables({"VAL": 3}))
    
    assert validator.validate_evaluation_periods() == 3
    assert not validator.issues_found


def test__validate_evaluation_periods__not_positive():
    config = {"evaluation-periods": "0"}
    validator = AwsAlarmValidator(config, Variables())
    
    validator.validate_evaluation_periods()
    
    assert validator.issues_found
    assert any("evaluation-periods" in issue for issue in validator.issues)


def test__validate_treat_missing_data__valid():
    valid_treatments = AwsAlarmValidator.VALID_MISSING_DATA_TREATMENTS
    
    for treatment in valid_treatments:
        config = {"treat-missing-data": treatment}
        validator = AwsAlarmValidator(config, Variables())
        
        assert validator.validate_treat_missing_data() == treatment
        assert not validator.issues_found


def test__validate_treat_missing_data__value_substituted():
    config = {"treat-missing-data": "$VAL"}
    validator = AwsAlarmValidator(config, Variables({"VAL": "notBreaching"}))
    
    assert validator.validate_treat_missing_data() == "notBreaching"
    assert not validator.issues_found


def test__validate_treat_missing_data__invalid():
    config = {"treat-missing-data": "invalidTreatment"}
    validator = AwsAlarmValidator(config, Variables())
    
    assert validator.validate_treat_missing_data() == ""
    assert validator.issues_found


def test__validate_alarm_actions__single_string():
    config = {"alarm-actions": "arn:aws:sns:us-east-1:123456789012:MyTopic"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_alarm_actions()
    
    assert result == ["arn:aws:sns:us-east-1:123456789012:MyTopic"]
    assert not validator.issues_found


def test__validate_alarm_actions__value_substituted():
    config = {"alarm-actions": "arn:aws:sns:us-east-1:$ACCOUNT_ID:MyTopic"}
    validator = AwsAlarmValidator(config, Variables({"ACCOUNT_ID": "1234"}))
    
    
    result = validator.validate_alarm_actions()
    
    
    assert isinstance(result, list)
    assert result == ["arn:aws:sns:us-east-1:1234:MyTopic"]
    assert not validator.issues_found


def test__validate_alarm_actions__list():
    actions = [
        "arn:aws:sns:us-east-1:123456789012:Topic1",
        "arn:aws:sns:us-east-1:123456789012:Topic2"
    ]
    config = {"alarm-actions": actions}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_alarm_actions()
    
    assert result == actions
    assert not validator.issues_found


def test__validate_alarm_actions__invalid_format():
    config = {"alarm-actions": ["invalid-arn"]}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_alarm_actions()
    
    assert result == ["invalid-arn"]
    assert validator.issues_found


def test__validate_tags__valid():
    tags = {"Environment": "Production", "Owner": "Team1"}
    config = {"tags": tags}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_tags()
    
    assert result == tags
    assert not validator.issues_found


def test__validate_tags__invalid_type():
    config = {"tags": "not-a-dict"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_tags()
    
    assert result == {}
    assert validator.issues_found
    assert any("Tags must be a dictionary" in issue for issue in validator.issues)


def test__validate_dimensions__valid():
    dimensions = {"InstanceId": "i-1234567890abcdef0"}
    config = {"dimensions": dimensions}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_dimensions()
    
    assert result == dimensions
    assert not validator.issues_found


def test__validate_dimensions__invalid_type():
    config = {"dimensions": "not-a-dict"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_dimensions()
    
    assert result == {}
    assert validator.issues_found
    assert any("Dimensions must be a dictionary" in issue for issue in validator.issues)


def test__validate_metric_name__valid():
    config = {"metric-name": "CPUUtilization"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_metric_name()
    
    assert result == "CPUUtilization"
    assert not validator.issues_found


def test__validate_metric_name__not_a_string():
    config = {"metric-name": 123}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_metric_name()
    
    assert result == ""
    assert validator.issues_found


def test__validate_metric_name__with_allowed_list():
    allowed_metrics = ["CPUUtilization", "MemoryUtilization"]
    
    config = {"metric-name": "CPUUtilization"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_metric_name(allowed=allowed_metrics)
    
    assert result == "CPUUtilization"
    assert not validator.issues_found


def test__validate_metric_name__not_in_allowed_list():
    allowed_metrics = ["CPUUtilization", "MemoryUtilization"]
    
    config = {"metric-name": "DiskUtilization"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_metric_name(allowed=allowed_metrics)
    
    assert result == ""
    assert validator.issues_found
    assert any("is not a valid metric name" in issue for issue in validator.issues)


def test__validate_alarm_name__valid():
    config = {"alarm-name": "High-CPU-Alarm"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_alarm_name()
    
    assert result == "High-CPU-Alarm"
    assert not validator.issues_found


def test__validate_alarm_name__not_a_string():
    config = {"alarm-name": 12312}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_alarm_name()
    
    assert result == ""
    assert validator.issues_found


def test__validate_alarm_name__with_variables():
    variables = Variables()
    variables.update({"SERVICE": "backend"})
    
    config = {"alarm-name": "$SERVICE-High-CPU-Alarm"}
    validator = AwsAlarmValidator(config, variables)
    
    result = validator.validate_alarm_name()
    
    assert result == "backend-High-CPU-Alarm"
    assert not validator.issues_found


def test__validate_alarm_name__name_to_long():
    config = {"alarm-name": "1" * 300}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_alarm_name()
    
    assert result == "1" * 300
    assert validator.issues_found


def test__validate_alarm_name__name_to_long_but_in_preview_mod():
    config = {"alarm-name": "1" * 300}
    validator = AwsAlarmValidator(config, Variables(), is_preview=True)
    
    result = validator.validate_alarm_name()
    
    assert result == "1" * 300
    assert not validator.issues_found


def test__validate_alarm_name__missing_variable():
    config = {"alarm-name": "$SERVICE-High-CPU-Alarm"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_alarm_name()
    
    assert result == "$SERVICE-High-CPU-Alarm"
    assert validator.issues_found
    assert any("Variable 'SERVICE' not found" in issue for issue in validator.issues)


def test__validate_threshold__valid_prc():
    config = {"threshold": "80%"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold()
    
    assert result == 80.0
    assert not validator.issues_found


def test__validate_threshold__string_stripped():
    config = {"threshold": "  80%   "}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold()
    
    assert result == 80.0
    assert not validator.issues_found


def test__validate_threshold__valid_suze():
    config = {"threshold": "123 KB"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold()
    
    assert result == 123.0 * 1024.0
    assert not validator.issues_found


def test__validate_threshold__valid_number():
    config = {"threshold": 600000000}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold()
    
    assert result == 600000000.0
    assert result != 60000000000.0
    assert not validator.issues_found


def test__validate_threshold__invalid_value():
    config = {"threshold": "abcd"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold()
    
    assert result == 0.0
    assert validator.issues_found


def test__validate_threshold__invalid_struct():
    config = {"threshold": [123]}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold()
    
    assert result == 0.0
    assert validator.issues_found


def test__validate_threshold__with_min_max():
    config = {"threshold": "50"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold(min_value=0, max_value=100)
    
    assert result == 50
    assert not validator.issues_found


def test__validate_threshold__below_min():
    config = {"threshold": "-10"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold(min_value=0)
    
    assert result == -10.0
    assert validator.issues_found
    assert any("threshold" in issue for issue in validator.issues)


def test__validate_threshold__above_max():
    config = {"threshold": "110"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_threshold(max_value=100)
    
    assert result == 110.0
    assert validator.issues_found
    assert any("threshold" in issue for issue in validator.issues)


def test__validate_unit__valid():
    valid_units = AwsAlarmValidator.VALID_UNITS
    
    for unit in valid_units:
        config = {"unit": unit}
        validator = AwsAlarmValidator(config, Variables())
        
        assert validator.validate_unit() == unit
        assert not validator.issues_found


def test__validate_unit__invalid():
    config = {"unit": "InvalidUnit"}
    validator = AwsAlarmValidator(config, Variables())
    
    validator.validate_unit()
    
    assert validator.issues_found
    assert any("Invalid unit" in issue for issue in validator.issues)


def test__validate_unit__value_substituted():
    config = {"unit": "$UNIT"}
    validator = AwsAlarmValidator(config, Variables({"UNIT": "Bits/Second"}))
    
    assert validator.validate_unit() == "Bits/Second"
    assert not validator.issues_found


def test__validate_namespace__valid():
    config = {"namespace": "AWS/EC2"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_namespace()
    
    assert result == "AWS/EC2"
    assert not validator.issues_found


def test__validate_namespace__not_a_string():
    config = {"namespace": 324}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_namespace()
    
    assert result == ""
    assert any("string" in issue for issue in validator.issues)


def test__validate_namespace__with_variables():
    variables = Variables()
    variables.update({"NAMESPACE": "AWS/EC2"})
    
    config = {"namespace": "$NAMESPACE"}
    validator = AwsAlarmValidator(config, variables)
    
    result = validator.validate_namespace()
    
    assert result == "AWS/EC2"
    assert not validator.issues_found


def test__validate_namespace__missing_variable():
    config = {"namespace": "$NAMESPACE"}
    validator = AwsAlarmValidator(config, Variables())
    
    result = validator.validate_namespace()
    
    assert result == "$NAMESPACE"
    assert validator.issues_found
    assert any("Variable 'NAMESPACE' not found" in issue for issue in validator.issues)


def test__validate_keys__all_required_present():
    required_keys = ["alarm-name", "namespace", "metric-name"]
    optional_keys = ["dimensions", "tags"]
    
    config = {
        "alarm-name": "test-alarm",
        "namespace": "AWS/EC2",
        "metric-name": "CPUUtilization"
    }
    
    validator = AwsAlarmValidator(config, Variables())
    validator.validate_keys(required_keys, optional_keys)
    
    assert not validator.issues_found


def test__validate_keys__missing_required():
    required_keys = ["alarm-name", "namespace", "metric-name"]
    optional_keys = ["dimensions", "tags"]
    
    config = {
        "alarm-name": "test-alarm",
        "namespace": "AWS/EC2"
    }
    
    validator = AwsAlarmValidator(config, Variables())
    validator.validate_keys(required_keys, optional_keys)
    
    assert validator.issues_found
    assert any("Missing required key 'metric-name'" in issue for issue in validator.issues)


def test__validate_keys__unknown_key():
    required_keys = ["alarm-name", "namespace", "metric-name"]
    optional_keys = ["dimensions", "tags"]
    
    config = {
        "alarm-name": "test-alarm",
        "namespace": "AWS/EC2",
        "metric-name": "CPUUtilization",
        "unknown-key": "value"
    }
    
    validator = AwsAlarmValidator(config, Variables())
    validator.validate_keys(required_keys, optional_keys)
    
    assert validator.issues_found
    assert any("Unknown key 'unknown-key'" in issue for issue in validator.issues)


def test__validate_keys__type_is_ignored():
    required_keys = ["alarm-name", "namespace", "metric-name"]
    optional_keys = ["dimensions", "tags"]
    
    config = {
        "alarm-name": "test-alarm",
        "namespace": "AWS/EC2",
        "metric-name": "CPUUtilization",
        "type": "EC2"
    }
    
    validator = AwsAlarmValidator(config, Variables())
    validator.validate_keys(required_keys, optional_keys)
    
    assert not validator.issues_found
