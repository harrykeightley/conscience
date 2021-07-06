#!/bin/bash
# helper script to run tests anywhere in the repo
# only for unix users - I don't know any bat

REPO_ROOT=$(git rev-parse --show-toplevel)

cd "${REPO_ROOT}" && python3 -m unittest discover tests
