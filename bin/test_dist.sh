#!/bin/sh

if [ ! -d "alertalot" ] || [ ! -f ".pylintrc" ]; then
    echo "Error: This script must be run from the parent directory of 'alertalot'"
    echo "Current directory: $(pwd)"
    exit 1
fi

rm -rf venv_test 2>/dev/null
rm -rf dist 2>/dev/null

python3.10 -m venv venv_test
source venv_test/bin/activate
pip install build twine
python -m build

twine check dist/*
pip install dist/alertalot-*-none-any.whl
alertalot --help

rm -r venv_test
rm -r dist
