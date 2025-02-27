import re

from pytimeparse.timeparse import timeparse


_PERCENT_REGEX = r"^[0-9]{1,2}(\.[0-9]+)?%$"


def try_percentage(value: str) -> float | None:
    if re.match(_PERCENT_REGEX, value):
        return float(value.strip('%')) / 100.0
    
    if value == '100%':
        return 1.0
    
    try:
        float_value = float(value)
        
        if 0.0 <= float_value <= 1.0:
            return float_value
    
    except ValueError:
        pass
    
    return None


def percentage(value: str) -> float:
    value = try_percentage(value)
    
    if value is None:
        raise ValueError(f"String '{value}', is not a valid percentage expression. Use 23.4% or 0.234 formats")
    
    return value


def try_str2time(value: str) -> int | None:
    return timeparse(value)


def str2time(value: str) -> int:
    value = try_str2time(value)
    
    if value is None:
        raise ValueError(f"String '{value}', is not a valid time expression")
    
    return value
