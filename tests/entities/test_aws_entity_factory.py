from unittest.mock import Mock

import pytest

from alertalot.generic.args_object import ArgsObject
from alertalot.generic.target_type import TargetType
from alertalot.entities.aws_entity_factory import AwsEntityFactory
from alertalot.entities.aws_ec2_entity import AwsEc2Entity
from alertalot.entities.aws_generic_entity import AwsGenericEntity


def test__aws_entity_factory__from_args__with_ec2_id():
    mock_args = Mock(spec=ArgsObject)
    mock_args.ec2_id = "i-0123456789abcdef0"
    
    result = AwsEntityFactory.from_args(mock_args)
    
    assert isinstance(result, AwsEc2Entity)


def test__aws_entity_factory__from_args__with_no_ids():
    mock_args = Mock(spec=ArgsObject)
    mock_args.ec2_id = None
    
    result = AwsEntityFactory.from_args(mock_args)
    
    assert result is None


def test__aws_entity_factory__from_type__with_string_ec2():
    result = AwsEntityFactory.from_type("ec2")
    
    assert isinstance(result, AwsEc2Entity)


def test__aws_entity_factory__from_type__with_enum_ec2():
    assert isinstance(AwsEntityFactory.from_type(TargetType.EC2), AwsEc2Entity)
    assert isinstance(AwsEntityFactory.from_type(TargetType.GENERIC), AwsGenericEntity)


def test__aws_entity_factory__from_type__with_invalid_string():
    with pytest.raises(ValueError, match="'invalid'"):
        AwsEntityFactory.from_type("invalid")


def test__aws_entity_factory__from_type__with_valid_but_not_implemented():
    with pytest.raises(NotImplementedError, match="Missing entity type"):
        mock_type = Mock(spec=TargetType)
        mock_type.value = "ec3"
        
        AwsEntityFactory.from_type(mock_type)
