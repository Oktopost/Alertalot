#!/bin/sh

# Run Unittests
echo "> Running Unittests: 'pytest --cov=alertalot --cov-report=html --cov-branch --cov-fail-under=40'"
create_horizontal_line
pytest --cov=alertalot --cov-report=html --cov-branch --cov-fail-under=40
