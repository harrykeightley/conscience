#!/bin/bash

TEST=../tests/hacker
RESULTS=results/hacker
METADATA=container/metadata

docker run --rm \
    -p 5900:5900 \
    -v ${PWD}/${TEST}:/autograder/submission \
    -v ${PWD}/${RESULTS}:/autograder/results \
    -v ${PWD}/${METADATA}:/autograder/metadata \
    braewebb/csse1001-2021s2a3:latest \
    bash -c "/autograder/run_autograder && cat /autograder/results/results.json"

cat ${PWD}/${RESULTS}/results.json | jq
