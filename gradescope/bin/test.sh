#!/bin/bash

TEST=../tests/hello_world
RESULTS=results/hello_world

docker run --rm \
    -p 5900:5900 \
    -v ${PWD}/${TEST}:/autograder/submission \
    -v ${PWD}/${RESULTS}:/autograder/results \
    braewebb/csse1001-2021s2a3:latest \
    bash -c "/autograder/run_autograder && cat /autograder/results/results.json"

cat ${PWD}/${RESULTS}/results.json | jq
