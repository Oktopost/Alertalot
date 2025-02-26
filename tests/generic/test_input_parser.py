import pytest

from alertalot.generic.input_parser import *


def test_percentage_valid():
    assert percentage("2%") == 0.02
    assert percentage("23%") == pytest.approx(0.23)
    assert percentage("23.4%") == pytest.approx(0.234)
    assert percentage("0.234") == pytest.approx(0.234)
    assert percentage("0.0") == pytest.approx(0.0)
    assert percentage("0") == 0
    assert percentage("100%") == 1.0
    assert percentage("1") == 1.0


def test_percentage_invalid():
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage("invalid")
    
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage("123abc")
    
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage("")
    
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage("-1%")


def test_try_percentage_valid():
    assert try_percentage("2%") == 0.02
    assert try_percentage("23%") == pytest.approx(0.23)
    assert try_percentage("23.4%") == pytest.approx(0.234)
    assert try_percentage("0.234") == pytest.approx(0.234)
    assert try_percentage("0.0") == pytest.approx(0.0)
    assert try_percentage("0") == 0
    assert try_percentage("100%") == 1.0
    assert try_percentage("1") == 1.0


def test_try_percentage_invalid():
    assert try_percentage("invalid") is None
    assert try_percentage("123abc") is None
    assert try_percentage("") is None
    assert try_percentage("-1%") is None


