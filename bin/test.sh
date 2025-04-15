#!/bin/sh

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
IS_FAILED=0

create_horizontal_line() {
  width=$(tput cols)
  line=""

  for ((i=0; i<$width; i++)); do
    line="${line}─"
  done

  echo "$line"
}

# Check if script is running from parent directory
if [ ! -d "alertalot" ] || [ ! -f ".pylintrc" ]; then
    echo "Error: This script must be run from the parent directory of 'alertalot'"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate


# Run pylint on alertalot
echo "> Running Pylint on Alertalot: 'pylint alertalot --rcfile=.pylintrc --fail-under=10'"
create_horizontal_line
pylint alertalot --rcfile=.pylintrc --fail-under=10
PYLINT_ALERTALOT_RESULT=$?

# Run pylint on unittests
echo "> Running Pylint on Unittests: 'pylint tests --rcfile=tests/.pylintrc --fail-under=10'"
create_horizontal_line
pylint tests --rcfile=tests/.pylintrc --fail-under=10
PYLINT_TESTS_RESULT=$?

# Run Unittests
echo "> Running Unittests: 'pytest --cov=alertalot --cov-report=html --cov-branch --cov-fail-under=40'"
create_horizontal_line
pytest --cov=alertalot --cov-report=html --cov-branch --cov-fail-under=40
UNITTESTS_RESULT=$?


create_horizontal_line

if [ $PYLINT_ALERTALOT_RESULT -eq 0 ]; then
  echo -e "${GREEN}✓${NC} SUCCESS: Alertalot Pylint check passed"
else
  echo -e "${RED}✗${NC} FAILURE: Alertalot Pylint check failed"
  IS_FAILED=1
fi

if [ $PYLINT_TESTS_RESULT -eq 0 ]; then
  echo -e "${GREEN}✓${NC} SUCCESS: Unittests Pylint check passed"
else
  echo -e "${RED}✗${NC} FAILURE: Unittests Pylint check failed"
  IS_FAILED=1
fi

if [ $UNITTESTS_RESULT -eq 0 ]; then
  echo -e "${GREEN}✓${NC} SUCCESS: Unittests passed"
else
  echo -e "${RED}✗${NC} FAILURE: Unittests failed"
  IS_FAILED=1
fi


create_horizontal_line

if [ $IS_FAILED -eq 0 ]; then
  echo -e "${GREEN}✓ OK!${NC}"
else
  echo -e "${RED}✗ Failed!${NC}"
  IS_FAILED=1
fi
