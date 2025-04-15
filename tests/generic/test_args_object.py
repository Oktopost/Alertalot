from unittest.mock import Mock, patch

from alertalot.generic.args_object import ArgsObject


def test__init__basic_args():
    mock_args = Mock()
    mock_args.verbose = True
    mock_args.quiet = False
    mock_args.show_variables = True
    mock_args.show_target = False
    mock_args.show_template = True
    mock_args.create_alarms = False
    mock_args.test_aws = True
    mock_args.trace = False
    mock_args.vars_file = "path/to/vars.yaml"
    mock_args.template_file = "path/to/template.yaml"
    mock_args.region = None
    mock_args.ec2_id = "i-1234567890abcdef0"
    mock_args.variables = {"ENV": "prod", "APP": "test"}
    mock_args.strict = True
    
    
    args_obj = ArgsObject(mock_args)
    
    
    assert args_obj.is_verbose is True
    assert args_obj.is_quiet is False
    assert args_obj.show_variables is True
    assert args_obj.show_target is False
    assert args_obj.show_template is True
    assert args_obj.create_alarms is False
    assert args_obj.test_aws is True
    assert args_obj.with_trace is False
    assert args_obj.vars_file == "path/to/vars.yaml"
    assert args_obj.template_file == "path/to/template.yaml"
    assert args_obj.region is None
    assert args_obj.ec2_id == "i-1234567890abcdef0"
    assert args_obj.variables == {"ENV": "prod", "APP": "test"}
    assert args_obj.is_strict is True


@patch('boto3.setup_default_session')
def test__init__with_region(mock_setup_session):
    mock_args = Mock()
    mock_args.region = "us-west-2"
    mock_args.variables = {}
    
    
    args_obj = ArgsObject(mock_args)
    
    
    assert args_obj.region == "us-west-2"
    mock_setup_session.assert_called_once_with(region_name="us-west-2")


def test__variables_conversion():
    mock_args = Mock()
    mock_args.variables = [("key1", "value1"), ("key2", "value2")]
    mock_args.region = None
    
    
    args_obj = ArgsObject(mock_args)
    
    
    assert isinstance(args_obj.variables, dict)
    assert args_obj.variables == {"key1": "value1", "key2": "value2"}
