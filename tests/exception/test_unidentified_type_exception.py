from alertalot.exception.unidentified_type_exception import UnidentifiedTypeException


def test__unidentified_type_exception__sanity():
    exception = UnidentifiedTypeException()
    
    assert "type" in str(exception)
    assert "config file" in str(exception)
    assert "entity arguments" in str(exception)
