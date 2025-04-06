"""Output formatting utilities."""
from typing import Dict, Any


def get_aligned_dict(
        dictionary: Dict[str, Any],
        padding: int = 0,
        sep: str = ":",
        margin_left: int = 1,
        margin_right: int = 1,
        newline: str = "\n") -> str:
    """
    Format a dictionary with aligned keys for consistent output.
    
    Args:
        dictionary: Dictionary to be formatted
        padding: Number of spaces to add at the beginning of each line
        sep: Separator character between keys and values
        margin_left: Number of spaces between key and separator
        margin_right: Number of spaces between separator and value
        newline: Character(s) to use for line breaks
        
    Returns:
        Formatted string with aligned dictionary entries
    """
    max_key_length = max(len(key) for key in dictionary.keys()) if dictionary else 0
    
    formatted_lines = []
    
    for key, value in dictionary.items():
        padding_str = " " * padding
        key_padding_str = " " * (max_key_length - len(key))
        ml_str = " " * margin_left
        mr_str = " " * margin_right
        
        formatted_lines.append(f"{padding_str}{key}{key_padding_str}{ml_str}{sep}{mr_str}{str(value)}")
    
    return newline.join(formatted_lines)