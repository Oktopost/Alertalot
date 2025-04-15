import re

from pytimeparse.timeparse import timeparse


_PERCENT_REGEX = r"^[0-9]{1,2}(\.[0-9]+)?%$"

_SIZE_UNITS_MULTIPLIERS = {
    '': 0,
    'b': 0,
    'byte': 0,
    'bytes': 0,
    'kb': 1,
    'kilobyte': 1,
    'kilobytes': 1,
    'mb': 2,
    'megabyte': 2,
    'megabytes': 2,
    'gb': 3,
    'gigabyte': 3,
    'gigabytes': 3,
    'tb': 4,
    'terabyte': 4,
    'terabytes': 4,
    'pb': 5,
    'petabyte': 5,
    'petabytes': 5
}


def try_percentage(value: str | float | int, mult: float = 1.0) -> float | None:
    """
    Attempts to convert a string to a percentage value.
    
    Args:
        value (str | float | int): String representation of a percentage
        mult (float):
            The value of 100%. The % value in string, will be multiplied by this value.
            If the value passed is not a string with %, no multiplication is done.
    
    Returns:
        float | None: The percentage as a float, or None if conversion fails
    """
    mult = float(mult)
    value = str(value)
    
    if re.match(_PERCENT_REGEX, value):
        return float(value.strip('%')) / 100.0 * mult
    
    if value == '100%':
        return 1.0 * mult
    
    try:
        return float(value)
    
    except ValueError:
        pass
    
    return None


def percentage(value: str | float | int, mult: float = 1.0) -> float:
    """
    Converts a string to a percentage value.
    
    Args:
        value (str | float | int): String representation of a percentage
        mult (float):
            The value of 100%. The % value in string, will be multiplied by this value.
            If the value passed is not a string with %, no multiplication is done.
    
    Returns:
        float: The percentage as a float value, 100% will be 100.0.
    
    Raises:
        ValueError: If the string cannot be converted to a percentage
    """
    parsed_value = try_percentage(value, mult)
    
    if parsed_value is None:
        raise ValueError(f"String '{value}', is not a valid percentage expression. Use 23.4% or 0.234 formats")
    
    return parsed_value


def try_str2time(value: str | int | float) -> int | float | None:
    """
    Attempts to convert a string time expression or int to seconds.

    Delegates to the timeparse function to handle various time formats
    like '1h30m', '90s', etc.
    
    If an integer or float is provided, it's treated as minutes and converted to seconds as integer.
    
    Args:
        value (str | int | float):
            String representation of a time duration, integer number of minutes, or float number of seconds.
    
    Returns:
        int | None: The time in seconds, or None if conversion fails
    """
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            pass
            
    if isinstance(value, (int, float)):
        return int(value * 60)
    
    return timeparse(str(value))


def str2time(value: str) -> int:
    """
    Converts a string time expression to seconds.
    
    Args:
        value (str): String representation of a time duration
    
    Returns:
        int: The time in seconds as an integer
    
    Raises:
        ValueError: If the string cannot be converted to a time value
    """
    parsed_value = try_str2time(value)
    
    if parsed_value is None:
        raise ValueError(f"String '{value}', is not a valid time expression")
    
    return parsed_value


def str2bytes(size_str: str, base: int = 1024) -> int:
    """
    Convert a size string into bytes as integer by parsing size units.
    
    Parse strings with various storage units (B, KB, MB, GB, TB, PB) and
    converts them to bytes. Handle inputs with or without spaces between
    value and unit. If no unit is specified, assumes the value is already in bytes.
    
    Args:
        size_str (str): Size string like '5 GB', '345 byte', etc.
        base (int): Base multiplier, either 1024 (default) or 1000
        
    Returns:
        int: Size in bytes
    """
    size_str = str(size_str)
    size_str = size_str.strip()
    
    split_index = 0
    
    for i, char in enumerate(size_str):
        if not (char.isdigit() or char == '.'):
            split_index = i
            break
    
    if split_index == 0:
        # No unit found, just a number
        return int(float(size_str))
    
    value = float(size_str[:split_index].strip())
    unit = size_str[split_index:].strip().lower()
    
    if unit not in _SIZE_UNITS_MULTIPLIERS:
        raise ValueError(f"Unrecognized unit: '{unit}'. Valid units are: b, byte, kb, mb, gb, tb, pb, etc.")
    
    multiplier = _SIZE_UNITS_MULTIPLIERS[unit]
    
    return int(value * (base ** multiplier))
