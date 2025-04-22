#!/bin/sh

if [ ! -d "alertalot" ] || [ ! -f ".pylintrc" ]; then
    echo "Error: This script must be run from the parent directory of 'alertalot'"
    echo "Current directory: $(pwd)"
    exit 1
fi

rm -rf venv_install_testpuypi 2>/dev/null
python3.10 -m venv venv_install_testpuypi
source venv_install_testpuypi/bin/activate

pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  alertalot

alertalot --help
deactivate
rm -rf venv_install_testpuypi 2>/dev/null
