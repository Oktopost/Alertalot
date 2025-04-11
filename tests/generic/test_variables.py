import pytest

from alertalot.generic.variables import *


def test__contains__empty_set():
    params = Variables()
    
    assert ("abc" in params) is False
    assert ("b" in params) is False
    assert ("" in params) is False
    

def test__contains__not_empty_set():
    params = Variables()
    
    params.update({"a": 1, "abc": "21"})
    
    assert ("a" in params) is True
    assert ("abc" in params) is True
    
    assert ("A" in params) is False
    assert ("ABC" in params) is False
    assert ("b" in params) is False
    assert ("" in params) is False


def test__getitem__():
    params = Variables()
    
    params.update({"a": 1, "abc": "21"})
    
    assert params["a"] == 1
    assert params["abc"] == "21"
    
    assert params["ABC"] is None
    assert params["missing"] is None

    
def test__update__pass_none():
    params = Variables()
    
    params.update({"a": "b"})
    
    assert params["a"] == "b"
    params.update(None)
    assert params["a"] == "b"


def test__update__pass_override_values():
    params = Variables()
    
    params.update({"a": "b", "c": "d"})
    
    assert params["a"] == "b"
    assert params["c"] == "d"
    
    params.update({"c": "n"})
    
    assert params["a"] == "b"
    assert params["c"] == "n"


def test__update__pass_new_values():
    params = Variables()
    
    params.update({"a": "b"})
    
    assert params["a"] == "b"
    assert params["c"] is None
    
    params.update({"c": "d"})
    
    assert params["a"] == "b"
    assert params["c"] == "d"


def test__update__pass_parameters_object():
    params1 = Variables()
    params1.update({"a": "b", "c": "d"})
    
    params2 = Variables()
    params2.update({"e": "f", "c": "g"})
    
    params1.update(params2)
    
    assert params1["a"] == "b"
    assert params1["c"] == "g"
    assert params1["e"] == "f"


def test__substitute_variables():
    parameters = Variables()
    parameters.update({"INSTANCE_ID": 123, "REGION": "us-east-1", "SERVICE": "backend"})
    
    assert parameters.substitute("") == ""
    assert parameters.substitute("$REGION") == "us-east-1"
    
    assert parameters.substitute("Instance: $INSTANCE_ID") == "Instance: 123"
    assert parameters.substitute("R: $REGION, S: $SERVICE") == "R: us-east-1, S: backend"
    assert parameters.substitute("No variables here.") == "No variables here."
    assert parameters.substitute("$SERVICE is running") == "backend is running"
    assert parameters.substitute("Service is $SERVICE") == "Service is backend"
    assert parameters.substitute("Service: $SERVICE.") == "Service: backend."
    assert parameters.substitute("Service: $SERVICE!") == "Service: backend!"
    assert parameters.substitute("$SERVICE, $SERVICE, $SERVICE") == "backend, backend, backend"


def test__substitute_variables__not_found():
    parameters = Variables()
    parameters.update({"INSTANCE_ID": 123, "REGION": "us-east-1", "SERVICE": "backend"})
    
    with pytest.raises(KeyError, match="Variable 'UNKNOWN' not found in parameters."):
        parameters.substitute("Unknown: $UNKNOWN")
    
    with pytest.raises(KeyError, match="Variable 'UNKNOWN' not found in parameters."):
        parameters.substitute("Instance: $INSTANCE_ID, Missing: $UNKNOWN")


def test__substitute_variables__empty_set():
    parameters = Variables()
    
    with pytest.raises(KeyError, match="Variable 'SERVICE' not found in parameters."):
        parameters.substitute("$SERVICE")
