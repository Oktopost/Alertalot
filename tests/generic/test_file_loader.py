from unittest.mock import mock_open, patch

import json
import yaml
import pytest

from alertalot.generic.file_loader import load, load_yaml, load_json


def test__load_yaml__valid_yaml():
    yaml_content = """
    params:
      global:
        key1: value1
      us-east-1:
        key2: value2
    """
    expected = {'params': {'global': {'key1': 'value1'}, 'us-east-1': {'key2': 'value2'}}}
    
    with patch('builtins.open', mock_open(read_data=yaml_content)):
        with patch('os.path.abspath', return_value='/fake/path/file.yaml'):
            result = load_yaml('file.yaml')
            
    assert result == expected


def test__load_yaml__empty_yaml():
    yaml_content = """
    
    """
    expected = None
    
    with patch('builtins.open', mock_open(read_data=yaml_content)):
        with patch('os.path.abspath', return_value='/fake/path/file.yaml'):
            result = load_yaml('file.yaml')
            
    assert result == expected


def test__load_json__valid_json():
    json_content = """
    {
      "params": {
        "global": {
          "key1": "value1"
        },
        "us-east-1": {
          "key2": "value2"
        }
      }
    }
    """
    expected = {'params': {'global': {'key1': 'value1'}, 'us-east-1': {'key2': 'value2'}}}
    
    with patch('builtins.open', mock_open(read_data=json_content)):
        with patch('os.path.abspath', return_value='/fake/path/file.json'):
            result = load_json('file.json')
            
    assert result == expected


def test__load__yaml_file():
    with patch('alertalot.generic.file_loader.load_yaml') as mock_load_yaml:
        mock_load_yaml.return_value = {'key': 'value'}
        with patch('os.path.splitext', return_value=('file', '.yaml')):
            result = load('file.yaml')
            
    assert result == {'key': 'value'}
    mock_load_yaml.assert_called_once()


def test__load__yml_file():
    with patch('alertalot.generic.file_loader.load_yaml') as mock_load_yaml:
        mock_load_yaml.return_value = {'key': 'value'}
        with patch('os.path.splitext', return_value=('file', '.yml')):
            result = load('file.yml')
            
    assert result == {'key': 'value'}
    mock_load_yaml.assert_called_once()


def test__load__json_file():
    with patch('alertalot.generic.file_loader.load_json') as mock_load_json:
        mock_load_json.return_value = {'key': 'value'}
        with patch('os.path.splitext', return_value=('file', '.json')):
            result = load('file.json')
            
    assert result == {'key': 'value'}
    mock_load_json.assert_called_once()


def test__load__unsupported_extension():
    with patch('os.path.splitext', return_value=('file', '.txt')):
        with pytest.raises(ValueError, match="Unsupported file extension: .txt"):
            load('file.txt')


def test__load_yaml__file_not_found():
    with patch('builtins.open', side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            load_yaml('nonexistent.yaml')


def test__load_json__file_not_found():
    with patch('builtins.open', side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            load_json('nonexistent.json')


def test__load_yaml__invalid_yaml():
    with patch('builtins.open', mock_open(read_data='invalid: yaml: format:')):
        with pytest.raises(yaml.YAMLError):
            load_yaml('invalid.yaml')


def test__load_json__invalid_json():
    with patch('builtins.open', mock_open(read_data='{"invalid": json')):
        with pytest.raises(json.JSONDecodeError):
            load_json('invalid.json')


def test__load_json__empty_file():
    with patch('builtins.open', mock_open(read_data='')):
        with pytest.raises(json.JSONDecodeError):
            load_json('empty.json')
