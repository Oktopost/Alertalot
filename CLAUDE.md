# CLAUDE.md

Guidance for Claude Code when working with this repository.

## Python Style Guide
- Follow Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
- **Imports**: Group imports by standard library, third-party, and local modules with blank lines between groups
- **Formatting**: 4-space indentation, 120 character line length
- **Error Handling**: Use specific exceptions with descriptive messages
- **Types**: Include type hints for parameters and return values
  - Use built-in types (e.g., `dict`, `list`) instead of imports from `typing` when possible
  - Only import types from `typing` when necessary (e.g., `Any`, `Union`)
- **Docstrings**: Use Google-style docstrings for modules, classes, and functions
  - Docstring summary should be on a new line after the opening triple quotes
  - Example: 
    ```python
    def some_function():
        """
        This is a docstring summary on a new line.
        
        More details here.
        """
    ```
- **Naming**: snake_case for functions/variables, CamelCase for classes, UPPER_CASE for constants
- **File Format**: Each file should end with exactly one empty line

## Examples and Configuration Files
- Examples in `examples/` directory (YAML and JSON configurations)
- Reference `examples/ec2-application.yaml` and `examples/params.yaml` for configuration
- JSON schemas in `schemes/` directory

## Testing Standards
- Tests in `tests/` directory mirroring package structure
- Files named `test_*.py`
- Functions named `test__function_name__test_case` 
- Use pytest fixtures for setup/teardown
- Tests should be independent
- Use parameterization for similar test cases
- Mock external dependencies when appropriate