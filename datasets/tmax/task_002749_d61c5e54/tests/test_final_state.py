# test_final_state.py

import os
import pytest

def test_output_file_exists():
    assert os.path.isfile("/home/user/pipeline_out/dataset.csv"), "Output file /home/user/pipeline_out/dataset.csv does not exist"

def test_output_file_content():
    expected_lines = [
        "event_id,user_id,age,signup_source,score_normalized",
        "101,1,25,web,55",
        "102,2,0,app,32",
        "103,2,0,app,81",
        "104,3,40,web,99",
        "105,4,0,app,10"
    ]

    with open("/home/user/pipeline_out/dataset.csv", "r") as f:
        # Read lines, strip whitespace/newlines, filter out empty lines
        actual_lines = [line.strip().replace(" ", "") for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} does not match expected output. Expected: '{expected}', Actual: '{actual}'"