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
from rich.traceback import Traceback

from alertalot.generic.parameters import Parameters


class OutputLevel(Enum):
    """
    Enum defining different output verbosity levels for logging or displaying messages.
    
    This enum determines when certain output content should be displayed based on the
    verbosity mode of the application.
    
    Attributes:
        VERBOSE: Content is displayed only when verbose mode is enabled.
        NORMAL: Content is displayed in normal operation mode.
        QUITE: Content is always displayed, even in quiet mode (typically used for errors).
    """
    VERBOSE = 1     # Display only if verbose mode is enabled
    NORMAL = 2      # Display in normal operation mode
    QUITE = 3       # Always display, even in quiet mode (errors, critical info)


class Output:
    def __init__(
            self,
            is_quiet: bool = False,
            is_verbose: bool = False,
            with_trace: bool = False,
            spinner_style: str = "bouncingBall",
            tables_style: box = box.MINIMAL):
        
        self.__is_first_step_printed = False
        
        self.__console = Console()
        
        self.__theme = "monokai"
        
        # Exceptions
        self.__with_trace = with_trace
        
        # Output level.
        self.__is_quiet = is_quiet
        self.__is_verbose = is_verbose
        
        self.__output_level = OutputLevel.NORMAL
        self.__define_output_level()
        
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
    
    
    def print(self, *objects: Any, level: OutputLevel = OutputLevel.NORMAL) -> None:
        """
        Print objects to the console.
        
        Args:
            *objects: Objects to print
            level (OutputLevel):
        """
        if not self.__check_level(level):
            return
        
        self.__console.print(*objects)
        
    def print_step(self, text: str, level: OutputLevel = OutputLevel.VERBOSE) -> None:
        """
        
        Args:
            text (str): Text to print
        """
        if not self.__check_level(level):
            return
        
        if not self.__is_first_step_printed:
            self.__is_first_step_printed = True
        else:
            self.__console.print("")
        
        self.print_line(level=level)
        self.__console.print(f"➤ [bold]{text}[/bold]")
        self.__console.print("")

    def print_success(self, *objects: Any, level: OutputLevel = OutputLevel.VERBOSE) -> None:
        self.print("[bold green]✓[/bold green]", *objects, level=level)
        
    def print_failure(self, *objects: Any, level: OutputLevel = OutputLevel.VERBOSE) -> None:
        self.print("[bold red]✗[/bold red]", *objects, level=level)
        
    def print_bullet(self, *objects: Any, level: OutputLevel = OutputLevel.VERBOSE) -> None:
        self.print("[bold blue]✦[/bold blue]", *objects, level=level)
    
    def print_line(self, level: OutputLevel = OutputLevel.VERBOSE, color: str = "Green") -> None:
        self.print(Rule(style=color), level=level)
    
    def print_if_verbose(self, *objects: Any) -> None:
        """
        Print objects to the console only if verbose mode enabled.
        
        Args:
            *objects: Objects to print
        """
        self.print(*objects, level=OutputLevel.VERBOSE)
    
    def print_list(
            self,
            symbol: str,
            symbol_style: str,
            data: list[str],
            level: OutputLevel = OutputLevel.NORMAL) -> None:
        
        if not self.__check_level(level):
            return
        
        self.__console.print("")
        
        for item in data:
            self.__console.print(f"  [{symbol_style}]{symbol}[/{symbol_style}]{item}")
        
        self.__console.print("")
    
    def print_key_value(
            self,
            data: dict | Parameters,
            title: str | None = None,
            level: OutputLevel = OutputLevel.NORMAL) -> None:
        """
        Print parameters in a formatted table.
        
        Args:
            data (dict | Parameters): Data to print as a table
            title (str | None): Title of the table
        """
        if not self.__check_level(level):
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
    
    def print_yaml(self, data, level: OutputLevel = OutputLevel.VERBOSE) -> None:
        """
        Print formatted YAML data.
        
        Args:
            data: The data to print.
            level (OutputLevel): Level of the output.
        """
        if not self.__check_level(level):
            return
        
        yaml_str = yaml.dump(data, default_flow_style=False, sort_keys=False)
        yaml_syntax = Syntax(yaml_str, "yaml", theme=self.__theme)
        
        self.__console.print(yaml_syntax)
    
    def print_error(self, exception: Exception, level: OutputLevel = OutputLevel.NORMAL) -> None:
        if not self.__check_level(level):
            return
        
        if self.__with_trace:
            traceback = Traceback.from_exception(type(exception), exception, exception.__traceback__)
            self.__console.print(traceback)
        else:
            self.print_failure(f"[bold red3]Exception:[/bold red3] {exception}", level=level)

    
    def __check_level(self, level: OutputLevel) -> bool:
        return level.value >= self.__output_level.value
    
    def __define_output_level(self):
        if self.__is_quiet:
            self.__output_level = OutputLevel.QUITE
        elif self.__is_verbose:
            self.__output_level = OutputLevel.VERBOSE
        else:
            self.__output_level = OutputLevel.NORMAL
