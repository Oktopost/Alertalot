from alertalot.generic.parameters import *


def test___contains___empty_set():
    params = Parameters()
    
    assert ("abc" in params) is False
    assert ("b" in params) is False
    assert ("" in params) is False
    

def test___contains___not_empty_set():
    params = Parameters()
    
    params.update({"a": 1, "abc": "21"})
    
    assert ("a" in params) is True
    assert ("abc" in params) is True
    
    assert ("A" in params) is False
    assert ("ABC" in params) is False
    assert ("b" in params) is False
    assert ("" in params) is False
