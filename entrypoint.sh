#!/bin/sh
set -e

cd tests/spreadsheetapi

export SERVICE_BASE_URL="$1"
# NOTE: use python -m pytest to invoke pytest since it adds the current
# directory to the python path
pipenv run python -m pytest
