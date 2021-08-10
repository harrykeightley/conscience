#!/bin/bash
# helper to setup with dependencies

REPO_ROOT=$(git rev-parse --show-toplevel)

cd "${REPO_ROOT}" && python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt

