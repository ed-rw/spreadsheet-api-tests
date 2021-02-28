#!/bin/sh
set -e

echo "PWD: ${PWD}"
echo "SERVICE_BASE_URL: $1"

cd /opt/tests/spreadsheetapi/

export SERVICE_BASE_URL="$1"
# NOTE: use python -m pytest to invoke pytest since it adds the current
# directory to the python path
python -m pytest
