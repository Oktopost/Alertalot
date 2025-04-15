import pytest

from alertalot.generic.target_type import TargetType


def test__target_type__ec2_value():
    assert TargetType.EC2.value == "ec2"


def test__target_type__has__valid_target():
    assert TargetType.has("ec2") is True


def test__target_type__has__invalid_target():
    assert TargetType.has("invalid_target") is False


def test__target_type__has__case_sensitive():
    assert TargetType.has("EC2") is False


def test__target_type__require__valid_target():
    result = TargetType.require("ec2")
    assert result == TargetType.EC2


def test__target_type__require__invalid_target():
    with pytest.raises(ValueError, match="'invalid_target'"):
        TargetType.require("invalid_target")


def test__target_type__require__case_sensitive():
    with pytest.raises(ValueError, match="'EC2'"):
        TargetType.require("EC2")
