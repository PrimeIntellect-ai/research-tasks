#!/bin/bash
set -e

mkdir -p /logs/verifier

cd /tests
python3 -m pytest test_final_state.py -v 2>&1 | tee /logs/verifier/test-stdout.txt
TEST_EXIT=${PIPESTATUS[0]}

if [ $TEST_EXIT -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
else
    echo 0 > /logs/verifier/reward.txt
fi

exit 0
