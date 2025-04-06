from alertalot.generic.output import get_aligned_dict


def test__get_aligned_dict__empty_dict():
    assert "" == get_aligned_dict({})


def test__get_aligned_dict__simple_dict():
    data = {"name": "test", "value": 123}
    
    result = get_aligned_dict(data)
    
    assert result == "name  : test\nvalue : 123"


def test__get_aligned_dict__with_padding():
    data = {"id": 1, "name": "test"}
    
    result = get_aligned_dict(data, padding=2)
    
    assert result == "  id   : 1\n  name : test"


def test__get_aligned_dict__custom_separator():
    data = {"id": 1, "name": "test"}
    
    result = get_aligned_dict(data, sep="->")
    
    assert result == "id   -> 1\nname -> test"


def test__get_aligned_dict__custom_margins():
    data = {"id": 1, "name": "test"}
    
    result = get_aligned_dict(data, margin_left=2, margin_right=3)
    
    assert result == "id    :   1\nname  :   test"


def test__get_aligned_dict__custom_newline():
    data = {"id": 1, "name": "test"}
    
    result = get_aligned_dict(data, newline="|")
    
    assert result == "id   : 1|name : test"


def test__get_aligned_dict__different_key_lengths():
    data = {"a": 1, "very_long_key": 2, "medium": 3}
    
    assert (get_aligned_dict(data) ==
            "a             : 1\n"
            "very_long_key : 2\n"
            "medium        : 3")



def test__get_aligned_dict__all_custom_parameters():
    data = {"id": 1, "name": "test"}
    
    result = get_aligned_dict(
        data, 
        padding=4, 
        sep="=", 
        margin_left=3, 
        margin_right=2, 
        newline="\r\n"
    )
    
    assert (result ==
            "    id     =  1\r\n"
            "    name   =  test")
