"""Output formatting utilities."""
from enum import Enum

import yaml
import time

from typing import Any, Callable

from rich import box
from rich.text import Text
from rich.rule import Rule
from rich.live import Live
from rich.table import Table
from rich.syntax import Syntax
from rich.spinner import Spinner
from rich.console import Console

from alertalot.generic.parameters import Parameters


class OutputType(Enum):
    VERBOSE = 1,
    ALWAYS = 2


class Output:
    def __init__(
            self,
            is_quiet: bool = False,
            is_verbose: bool = False,
            spinner_style: str = "bouncingBall",
            tables_style: box = box.MINIMAL):
        
        self.__is_first_step_printed = False
        
        self.__console = Console()
        
        self.__theme = "monokai"
        
        self.__is_quiet = is_quiet
        self.__is_verbose = is_verbose
        
        # Spinner
        self.__spinners_style = spinner_style
        
        # Table
        self.__tables_title_style = "bold"
        self.__tables_style = tables_style
    
    
    @property
    def is_verbose(self) -> bool:
        """
        Check if verbose mode is enabled.
        
        Returns:
            bool: Whether verbose mode is enabled.
        """
        return self.__is_verbose
    
    
    def print(self, *objects: Any, type: OutputType = OutputType.ALWAYS) -> None:
        """
        Print objects to the console.
        
        Args:
            type:
            *objects: Objects to print
            type (OutputType):
        """
        if self.__is_quiet:
            return
        if type == OutputType.VERBOSE and not self.__is_verbose:
            return
        
        self.__console.print(*objects)
        
    def print_step(self, text: str, type: OutputType = OutputType.VERBOSE) -> None:
        """
        
        Args:
            text (str): Text to print
        """
        if not self.__is_first_step_printed:
            self.__is_first_step_printed = True
        else:
            self.print("", type=type)
        
        self.print_line(type=type)
        self.print(f"➤ [bold]{text}[/bold]", type=type)
        self.print("", type=type)

    def print_success(self, *objects: Any, type: OutputType = OutputType.VERBOSE) -> None:
        self.print("[bold green]✓[/bold green]", *objects, type=type)
        
    def print_failure(self, *objects: Any, type: OutputType = OutputType.VERBOSE) -> None:
        self.print("[bold red]✗[/bold red]", *objects, type=type)
        
    def print_bullet(self, *objects: Any, type: OutputType = OutputType.VERBOSE) -> None:
        self.print("[bold blue]✦[/bold blue]", *objects, type=type)
    
    def print_line(self, type: OutputType = OutputType.VERBOSE) -> None:
        self.print(Rule(), type=type)
    
    def print_if_verbose(self, *objects: Any) -> None:
        """
        Print objects to the console only if verbose mode enabled.
        
        Args:
            *objects: Objects to print
        """
        self.print(*objects, type=OutputType.VERBOSE)
    
    def print_list(self, symbol: str, symbol_style: str, data: list[str]) -> None:
        table = Table(
            show_header=False,
            box=self.__tables_style)
        
        for item in data:
            table.add_row(f"[{symbol_style}]{symbol}[/{symbol_style}]{item}")
        
        self.__console.print(table)
    
    def print_key_value(self, data: dict | Parameters, title: str | None = None) -> None:
        """
        Print parameters in a formatted table.
        
        Args:
            data (dict | Parameters): Data to print as a table
            title (str | None): Title of the table
        """
        if self.__is_quiet:
            return
        
        table = Table(
            show_header=False,
            box=self.__tables_style)
        
        if title is not None:
            table.title = title
            table.title_style = self.__tables_title_style
        
        for key, value in data.items():
            bold_key = Text(str(key), style="bold")
            table.add_row(bold_key, str(value))
        
        self.__console.print(table)
    
    def spinner(self, callback: Callable[[], Any], with_time: bool = True) -> Any:
        """
        
        Args:
            callback (Callable): Callback to execute
            with_time (bool):
                If set, print the total time it took to execute the callback. Ignored if
                verbose mode is disabled AND it took more than 0.001 seconds.
        """
        if self.__is_quiet:
            return callback()
        
        spinner = Spinner(self.__spinners_style)
        start_time = time.time()
        
        with Live(spinner, console=self.__console, transient=not self.__is_verbose):
            result = callback()
        
        if with_time:
            self.print_if_verbose(f"Completed in {time.time() - start_time:.2f} seconds")
        
        return result
    
    def print_yaml(self, data, type: OutputType = OutputType.VERBOSE) -> None:
        """
        Print formatted YAML data.
        
        Args:
            data: The data to print.
            type (OutputType): Type of the output.
        """
        if not self.is_verbose and type == OutputType.VERBOSE:
            return
        elif self.__is_quiet:
            return
        
        yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
        yaml_syntax = Syntax(yaml_str, "yaml", theme=self.__theme)
        
        self.__console.print(yaml_syntax)
    
    def print_error(self, exception: Exception, type: OutputType = OutputType.ALWAYS) -> None:
        pass
