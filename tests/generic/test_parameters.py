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
    
    assert params["a"] is 1
    assert params["abc"] is "21"
    
    assert params["ABC"] is None
    assert params["missing"] is None

    
def test_update__pass_none():
    params = Parameters()
    
    params.update({"a": "b"})
    
    assert params["a"] is "b"
    params.update(None)
    assert params["a"] is "b"


def test_update__pass_override_values():
    params = Parameters()
    
    params.update({"a": "b", "c": "d"})
    
    assert params["a"] is "b"
    assert params["c"] is "d"
    
    params.update({"c": "n"})
    
    assert params["a"] is "b"
    assert params["c"] is "n"


def test_update__pass_new_values():
    params = Parameters()
    
    params.update({"a": "b"})
    
    assert params["a"] is "b"
    assert params["c"] is None
    
    params.update({"c": "d"})
    
    assert params["a"] is "b"
    assert params["c"] is "d"
   

def test_as_string__empty():
    params = Parameters()
    
    assert params.as_string() == "-empty-"


def test_as_string__has_data():
    params = Parameters()
    
    params.update({"a": "b", "e": "f", "long": "value", "srt": "value"})
    
    assert params.as_string() == \
           f"a    : b{os.linesep}" \
           f"e    : f{os.linesep}" \
           f"long : value{os.linesep}" \
           f"srt  : value"
