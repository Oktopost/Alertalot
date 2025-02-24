import re

from pytimeparse.timeparse import timeparse


_PERCENT_REGEX = r"^[0-9]{1,2}(\.[0-9]+)?%$"


def try_percentage(input: str) -> float|None:
	if re.match(_PERCENT_REGEX, input):
		return float(input.strip('%')) / 100.0
	
	try:
		float_value = float(input)
		
		if 0.0 <= float_value <= 1.0:
			return float_value
		
	except ValueError:
		pass
	
	return None

def percentage(input: str) -> float:
	value = try_percentage(input)
	
	if value is None:
		raise ValueError(f"String '{input}', is not a valid percentage expression. Use 23.4% or 0.234 formats")
	
	return value

def try_str2time(input: str) -> int|None:
	return timeparse(input)

def str2time(input: str) -> int:
	value = try_str2time(input)
	
	if value is None:
		raise ValueError(f"String '{input}', is not a valid time expression")
	
	return value