#!/bin/sh

# Check if script is running from parent directory
if [ ! -d "alertalot" ] || [ ! -f ".pylintrc" ]; then
    echo "Error: This script must be run from the parent directory of 'alertalot'"
    echo "Current directory: $(pwd)"
    exit 1
fi

python3.10 -m venv venv
pip install -e .[dev]
source venv/bin/activate
