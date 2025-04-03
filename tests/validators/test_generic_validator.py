import pytest

from alertalot.validators.generic_validator import (
    validate_comparison_operator,
    VALID_COMPARISON_OPERATORS
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
    assert "<at 'comparison-operator'>" in issues


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

