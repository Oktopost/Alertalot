#!/bin/sh

if [ ! -d "alertalot" ] || [ ! -f ".pylintrc" ]; then
    echo "Error: This script must be run from the parent directory of 'alertalot'"
    echo "Current directory: $(pwd)"
    exit 1
fi

rm -rf venv_dist_local 2>/dev/null
rm -rf dist 2>/dev/null

python3.10 -m venv venv_dist_local
source venv_dist_local/bin/activate
pip install build twine
python -m build

twine check dist/*
pip install dist/alertalot-*-none-any.whl
alertalot --help

rm -r venv_dist_local
rm -r dist
