import pytest

from alertalot.generic.input_parser import *


def test__percentage__valid():
    assert percentage("2%") == 0.02
    assert percentage("23%") == pytest.approx(0.23)
    assert percentage("23.4%") == pytest.approx(0.234)
    assert percentage("0.234") == pytest.approx(0.234)
    assert percentage("0.0") == pytest.approx(0.0)
    assert percentage("0") == 0
    assert percentage("100%") == 1.0
    assert percentage("1") == 1.0


def test__percentage__invalid():
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage("invalid")
    
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage("123abc")
    
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage("")
    
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage("-1%")


# noinspection PyTypeChecker
def test__percentage__non_string_input():
    assert percentage(0.5) == 0.5
    assert percentage(1) == 1.0
    assert percentage(0) == 0.0
    assert percentage(0.234) == pytest.approx(0.234)
    
    with pytest.raises(ValueError, match="is not a valid percentage expression"):
        percentage(23)


def test__try_percentage__valid():
    assert try_percentage("2%") == 0.02
    assert try_percentage("23%") == pytest.approx(0.23)
    assert try_percentage("23.4%") == pytest.approx(0.234)
    assert try_percentage("0.234") == pytest.approx(0.234)
    assert try_percentage("0.0") == pytest.approx(0.0)
    assert try_percentage("0") == 0
    assert try_percentage("100%") == 1.0
    assert try_percentage("1") == 1.0


def test__try_percentage__invalid():
    assert try_percentage("invalid") is None
    assert try_percentage("123abc") is None
    assert try_percentage("") is None
    assert try_percentage("-1%") is None


# noinspection PyTypeChecker
def test__try_percentage__non_string_input():
    assert try_percentage(0.5) == 0.5
    assert try_percentage(1) == 1.0
    assert try_percentage(0) == 0.0
    assert try_percentage(0.234) == pytest.approx(0.234)
    assert try_percentage(23) is None


def test__try_str2time__valid_inputs():
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


def test__try_str2time__invalid_inputs():
    assert try_str2time("") is None
    assert try_str2time("invalid") is None
    assert try_str2time("h30m") is None
    assert try_str2time("1x") is None
    assert try_str2time("thirty minutes") is None
    assert try_str2time("one hour") is None


# noinspection PyTypeChecker
def test__try_str2time__non_string_input():
    one_minute = 1
    one_hour = 60
    
    assert try_str2time(one_minute) == 1 * 60
    assert try_str2time(one_hour) == 60 * 60
    assert try_str2time(1.5) == int(1.5 * 60)
    assert try_str2time(0) == 0


def test__try_str2time__string_int_as_minutes():
    assert try_str2time("2") == 2 * 60
    assert try_str2time("60") == 60 * 60
    assert try_str2time("0") == 0
    assert try_str2time("1440") == 1440 * 60
    assert try_str2time("10.5") == 10 * 60 + 30


def test__str2time__valid_inputs():
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


def test__str2time__raises_for_invalid_inputs():
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


def test__str2time__error_message():
    with pytest.raises(ValueError, match="String 'None', is not a valid time expression"):
        str2time("invalid")


# noinspection PyTypeChecker
def test__str2time__non_string_input():
    assert str2time(1) == 1 * 60
    assert str2time(60) == 60 * 60
    assert str2time(1.5) == 30 + 60
    assert str2time(0) == 0


def test__str2time__string_int_as_minutes():
    assert str2time("2") == 2 * 60
    assert str2time("60") == 60 * 60
    assert str2time("0") == 0
    assert str2time("1440") == 1440 * 60


# noinspection PyTypeChecker
def test__str2time__int_as_minutes():
    assert str2time(5) == 5 * 60
    assert str2time(60) == 60 * 60
    assert str2time(0) == 0
    assert str2time(1440) == 1440 * 60


def test__try_str2time__times():
    assert try_str2time("1.5h") == 60 * 60 + 30 * 60
    assert try_str2time("1.5 hours") == 60 * 60 + 30 * 60
    assert try_str2time("0.5h") == 30 * 60
    assert try_str2time("1h 0.5m") == 60 * 60 + 30


def test__try_str2time__int_as_minutes():
    assert try_str2time(5) == 5 * 60
    assert try_str2time(60) == 60 * 60
    assert try_str2time(0) == 0
    assert try_str2time(1440) == 1440 * 60


def test__str2time__times():
    assert str2time("1.5h") == 60 * 60 + 30 * 60
    assert str2time("1.5 hours") == 60 * 60 + 30 * 60
    assert str2time("0.5h") == 30 * 60
    assert str2time("1h 0.5m") == 60 * 60 + 30


def test__str2bytes__numeric_input():
    assert str2bytes("123") == 123
    assert str2bytes("123.5") == 123


# noinspection PyTypeChecker
def test__str2bytes__non_string_input():
    assert str2bytes(123) == 123
    assert str2bytes(123.5) == 123
    assert str2bytes(0) == 0
    assert str2bytes(1024) == 1024


def test__str2bytes__byte_units():
    assert str2bytes("345 byte") == 345
    assert str2bytes("345 b") == 345
    assert str2bytes("345bytes") == 345
    assert str2bytes("345 BYTES") == 345


def test__str2bytes__kilobyte_units():
    assert str2bytes("89 kB") == 89 * 1024
    assert str2bytes("98 Kb") == 98 * 1024
    assert str2bytes("1kb") == 1 * 1024
    assert str2bytes("1 kilobyte") == 1 * 1024
    assert str2bytes("1.5 KB") == 1.5 * 1024


def test__str2bytes__megabyte_units():
    assert str2bytes("5 MB") == 5 * 1024**2
    assert str2bytes("2.5mb") == 2.5 * 1024**2
    assert str2bytes("1 megabyte") == 1 * 1024**2


def test__str2bytes__gigabyte_units():
    assert str2bytes("1 GB") == 1 * 1024**3
    assert str2bytes("0.5gb") == 0.5 * 1024**3


def test__str2bytes__terabyte_units():
    assert str2bytes("1 TB") == 1 * 1024**4


def test__str2bytes__petabyte_units():
    assert str2bytes("0.1 PB") == int(0.1 * 1024**5)


def test__str2bytes__base_1000():
    assert str2bytes("1 KB", base=1000) == 1 * 1000**1
    assert str2bytes("1 MB", base=1000) == 1 * 1000**2
    assert str2bytes("1 GB", base=1000) == 1 * 1000**3


def test__str2bytes__no_space():
    assert str2bytes("5MB") == 5 * 1024**2
    assert str2bytes("10GB") == 10 * 1024**3


def test__str2bytes__mixed_case():
    assert str2bytes("5 Mb") == 5 * 1024**2
    assert str2bytes("10 gB") == 10 * 1024**3
