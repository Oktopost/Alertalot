#!/bin/sh

if [ ! -d "alertalot" ] || [ ! -f ".pylintrc" ]; then
    echo "Error: This script must be run from the parent directory of 'alertalot'"
    echo "Current directory: $(pwd)"
    exit 1
fi

rm -rf venv_dist 2>/dev/null
rm -rf dist 2>/dev/null

python3.10 -m venv venv_dist
source venv_dist/bin/activate
pip install build
python -m build

twine check dist/*
twine upload --repository testpypi dist/*

rm -r venv_dist
rm -r dist
