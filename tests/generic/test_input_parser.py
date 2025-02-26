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


def test_try_str2time_valid_inputs():
    assert try_str2time("1h") == 60 * 60
    assert try_str2time("30m") == 30 * 60
    assert try_str2time("1h30m") == 60 * 60 + 30 * 60
    assert try_str2time("45s") == 45
    assert try_str2time("1h20m 30 seconds") == 60 * 60 + 20 * 60 + 30
    assert try_str2time("1d") == 24 * 60 * 60
    assert try_str2time("1d12h") == 24 * 60 * 60 + 12 * 60 * 60
    assert try_str2time("0m") == 0
    assert try_str2time("10 minutes") == 10 * 60
    assert try_str2time("10 minute") == 10 * 60


def test_try_str2time_invalid_inputs():
    assert try_str2time("") is None
    assert try_str2time("invalid") is None
    assert try_str2time("h30m") is None
    assert try_str2time("1x") is None
    assert try_str2time("thirty minutes") is None
    assert try_str2time("one hour") is None


def test_str2time_valid_inputs():
    assert str2time("1h") == 60 * 60
    assert str2time("30m") == 30 * 60
    assert str2time("1h30m") == 60 * 60 + 30 * 60
    assert str2time("45s") == 45
    assert str2time("1h20m 30 seconds") == 60 * 60 + 20 * 60 + 30
    assert str2time("1d") == 24 * 60 * 60
    assert str2time("1d12h") == 24 * 60 * 60 + 12 * 60 * 60
    assert str2time("0m") == 0
    assert str2time("10 minutes") == 10 * 60
    assert str2time("10 minute") == 10 * 60


def test_str2time_raises_for_invalid_inputs():
    with pytest.raises(ValueError):
        str2time("")
    
    with pytest.raises(ValueError):
        str2time("invalid")
    
    with pytest.raises(ValueError):
        str2time("h30m")
    
    with pytest.raises(ValueError):
        str2time("1x")
    
    with pytest.raises(ValueError):
        str2time("thirty minutes")
    
    with pytest.raises(ValueError):
        str2time("one hour")


def test_str2time_error_message():
    with pytest.raises(ValueError, match="String 'None', is not a valid time expression"):
        str2time("invalid")


def test_fractional_times():
    assert try_str2time("1.5h") == 60 * 60 + 30 * 60
    assert try_str2time("1.5 hours") == 60 * 60 + 30 * 60
    assert try_str2time("0.5h") == 30 * 60
    assert try_str2time("1h 0.5m") == 60 * 60 + 30
    
    assert str2time("1.5h") == 60 * 60 + 30 * 60
    assert str2time("1.5 hours") == 60 * 60 + 30 * 60
    assert str2time("0.5h") == 30 * 60
    assert str2time("1h 0.5m") == 60 * 60 + 30
