#!/bin/sh

if [ ! -d "alertalot" ] || [ ! -f ".pylintrc" ]; then
    echo "Error: This script must be run from the parent directory of 'alertalot'"
    echo "Current directory: $(pwd)"
    exit 1
fi


python3.10 -m venv venv
pip install -e .[dev]


# Get the version string like v1.2.3 from pyproject.toml
configured_version="v$(pip show alertalot | grep Version | cut -d ' ' -f2)"

# The version passed as argument.
tag_version="$(git describe --tags --exact-match HEAD | grep -E "v[0-9]+\.[0-9]+\.[0-9]+")"


if [ -z "$tag_version" ]; then
    echo "Error: Missing tag version"
    exit 1
fi

echo "pyproject.toml : $configured_version"
echo "git tag        : $tag_version"


if [ "$configured_version" = "$tag_version" ]; then
    echo "Version matches expected: $configured_version"
    exit 0
else
    echo "Version mismatch. Found: $configured_version, Expected: $tag_version"
    exit 1
fi
