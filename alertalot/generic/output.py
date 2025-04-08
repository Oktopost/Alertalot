"""Output formatting utilities."""
import yaml

from typing import  Any
from rich.syntax import Syntax

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from alertalot.generic.parameters import Parameters


def get_aligned_dict(
        dictionary: dict[str, Any],
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


def print_yaml(data: dict[str, Any]) -> None:
    yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
    yaml_syntax = Syntax(yaml_str, "yaml", theme="monokai", line_numbers=False)
    
    console = Console()
    console.print(yaml_syntax)


class Output:
    def __init__(
            self,
            is_verbose: bool = False,
            spinner_style: str = "bouncingBall",
            tables_style: box = box.MINIMAL):
        
        self.__console = Console()
        
        self.__theme = "monokai"
        
        self.__is_verbose = is_verbose
        self.__spinners_style = spinner_style
        self.__tables_style = tables_style
    
    
    @property
    def is_verbose(self) -> bool:
        """
        Check if verbose mode is enabled.
        
        Returns:
            bool: Whether verbose mode is enabled.
        """
        return self.__is_verbose
    
    def print(self, *objects: Any) -> None:
        """
        Print objects to the console.
        
        Args:
            *objects: Objects to print
        """
        self.__console.print(*objects)
    
    def print_if_verbose(self, *objects: Any) -> None:
        """
       Print objects to the console only if verbose mode enabled.
        
        Args:
            *objects: Objects to print
        """
        if self.is_verbose:
            self.__console.print(*objects)
    
    def print_parameters(self, parameters: Parameters) -> None:
        """
        Print parameters in a formatted table.
        
        Args:
            parameters (Parameters): Parameters object containing key-value pairs to display
        """
        table = Table(show_header=False, box=self.__tables_style)
        
        for key, value in parameters:
            bold_key = Text(str(key), style="bold")
            table.add_row(bold_key, str(value))
        
        self.__console.print(table)
    
    def print_yaml(self, data) -> None:
        """
        Print formatted YAML data.
        
        Args:
            data: The data to print.
        """
        yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
        yaml_syntax = Syntax(yaml_str, "yaml", theme=self.__theme)
        
        self.__console.print(yaml_syntax)
