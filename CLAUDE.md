# CLAUDE.md

Guidance for Claude Code when working with this repository.

## Python Style Guide
- Follow Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
- **Imports**: Group imports by standard library, third-party, and local modules with blank lines between groups
- **Formatting**: 4-space indentation, 120 character line length
- **Error Handling**: Use specific exceptions with descriptive messages
- **Types**: Include type hints for parameters and return values
- **Docstrings**: Use Google-style docstrings for modules, classes, and functions
- **Naming**: snake_case for functions/variables, CamelCase for classes, UPPER_CASE for constants

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