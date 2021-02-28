#!/bin/sh

cd spreadsheetapi

# TODO set env var for SERVICE_BASE_URL
export SERVICE_BASE_URL="$1"
# NOTE: use python -m pytest to invoke pytest since it adds the current
# directory to the python path
pipenv run python -m pytest
