import pytest

from alertalot.generic.parameters import *


def test__contains__empty_set():
    params = Parameters()
    
    assert ("abc" in params) is False
    assert ("b" in params) is False
    assert ("" in params) is False
    

def test__contains__not_empty_set():
    params = Parameters()
    
    params.update({"a": 1, "abc": "21"})
    
    assert ("a" in params) is True
    assert ("abc" in params) is True
    
    assert ("A" in params) is False
    assert ("ABC" in params) is False
    assert ("b" in params) is False
    assert ("" in params) is False


def test__getitem__():
    params = Parameters()
    
    params.update({"a": 1, "abc": "21"})
    
    assert params["a"] == 1
    assert params["abc"] == "21"
    
    assert params["ABC"] is None
    assert params["missing"] is None

    
def test__update__pass_none():
    params = Parameters()
    
    params.update({"a": "b"})
    
    assert params["a"] == "b"
    params.update(None)
    assert params["a"] == "b"


def test__update__pass_override_values():
    params = Parameters()
    
    params.update({"a": "b", "c": "d"})
    
    assert params["a"] == "b"
    assert params["c"] == "d"
    
    params.update({"c": "n"})
    
    assert params["a"] == "b"
    assert params["c"] == "n"


def test__update__pass_new_values():
    params = Parameters()
    
    params.update({"a": "b"})
    
    assert params["a"] == "b"
    assert params["c"] is None
    
    params.update({"c": "d"})
    
    assert params["a"] == "b"
    assert params["c"] == "d"
   

def test__as_string__empty():
    params = Parameters()
    
    assert params.as_string() == "-empty-"


def test__as_string__has_data():
    params = Parameters()
    
    params.update({"a": "b", "e": "f", "long": "value", "srt": "value"})
    
    assert params.as_string() == \
           f"a    : b{os.linesep}" \
           f"e    : f{os.linesep}" \
           f"long : value{os.linesep}" \
           f"srt  : value"


def test__substitute_variables():
    parameters = Parameters()
    parameters.update({"INSTANCE_ID": 123, "REGION": "us-east-1", "SERVICE": "backend"})
    
    assert parameters.substitute_variables("") == ""
    assert parameters.substitute_variables("$REGION") == "us-east-1"
    
    assert parameters.substitute_variables("Instance: $INSTANCE_ID") == "Instance: 123"
    assert parameters.substitute_variables("R: $REGION, S: $SERVICE") == "R: us-east-1, S: backend"
    assert parameters.substitute_variables("No variables here.") == "No variables here."
    assert parameters.substitute_variables("$SERVICE is running") == "backend is running"
    assert parameters.substitute_variables("Service is $SERVICE") == "Service is backend"
    assert parameters.substitute_variables("Service: $SERVICE.") == "Service: backend."
    assert parameters.substitute_variables("Service: $SERVICE!") == "Service: backend!"
    assert parameters.substitute_variables("$SERVICE, $SERVICE, $SERVICE") == "backend, backend, backend"


def test__substitute_variables__not_found():
    parameters = Parameters()
    parameters.update({"INSTANCE_ID": 123, "REGION": "us-east-1", "SERVICE": "backend"})
    
    with pytest.raises(KeyError, match="Variable 'UNKNOWN' not found in parameters."):
        parameters.substitute_variables("Unknown: $UNKNOWN")
    
    with pytest.raises(KeyError, match="Variable 'UNKNOWN' not found in parameters."):
        parameters.substitute_variables("Instance: $INSTANCE_ID, Missing: $UNKNOWN")


def test__substitute_variables__empty_set():
    parameters = Parameters()
    
    with pytest.raises(KeyError, match="Variable 'SERVICE' not found in parameters."):
        parameters.substitute_variables("$SERVICE")
