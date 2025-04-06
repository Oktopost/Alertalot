import pytest
from alertalot.generic.resource_values import get_ec2_values


def test__get_ec2_values__with_name_tag():
    mock_resource = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-123456789abcdef",
                        "Tags": [
                            {
                                "Key": "Name",
                                "Value": "test-instance"
                            },
                            {
                                "Key": "Environment",
                                "Value": "test"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    result = get_ec2_values(mock_resource)
    
    assert result["$INSTANCE_ID"] == "i-123456789abcdef"
    assert result["$INSTANCE_NAME"] == "test-instance"
    assert len(result) == 2


def test__get_ec2_values__without_name_tag():
    mock_resource = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-123456789abcdef",
                        "Tags": [
                            {
                                "Key": "Environment",
                                "Value": "test"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    result = get_ec2_values(mock_resource)
    
    assert result["$INSTANCE_ID"] == "i-123456789abcdef"
    assert "$INSTANCE_NAME" not in result
    assert len(result) == 1


def test__get_ec2_values__with_empty_tags():
    # Test when instance has no tags
    mock_resource = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-123456789abcdef",
                        "Tags": []
                    }
                ]
            }
        ]
    }
    
    result = get_ec2_values(mock_resource)
    
    assert result["$INSTANCE_ID"] == "i-123456789abcdef"
    assert "$INSTANCE_NAME" not in result
    assert len(result) == 1


def test__get_ec2_values__with_no_tags_field():
    mock_resource = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-123456789abcdef"
                    }
                ]
            }
        ]
    }
    
    with pytest.raises(KeyError) as excinfo:
        get_ec2_values(mock_resource)
    
    assert "Tags" in str(excinfo.value)


def test__get_ec2_values__malformed_resource():
    mock_resource = {
        "Reservations": []
    }
    
    with pytest.raises(IndexError):
        get_ec2_values(mock_resource)
