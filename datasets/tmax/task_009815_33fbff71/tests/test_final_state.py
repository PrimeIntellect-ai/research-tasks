# test_final_state.py

import os
import pytest

def test_pipeline_files_exist():
    assert os.path.isfile("/home/user/filter.c"), "Missing /home/user/filter.c"
    assert os.path.isfile("/home/user/pipeline.sh"), "Missing /home/user/pipeline.sh"
    assert os.access("/home/user/pipeline.sh", os.X_OK), "/home/user/pipeline.sh is not executable"

def test_clean_jsonl_output():
    clean_file = "/home/user/clean.jsonl"
    assert os.path.isfile(clean_file), f"Missing required output file: {clean_file}"

    with open(clean_file, "r") as f:
        content = f.read().strip()

    expected_lines = [
        r'{"ts":"2023-10-01T10:00:00Z","user":"admin","key":"database","val":"mysql"}',
        r'{"ts":"2023-10-01T10:05:00Z","user":"admin","key":"password","val":"***"}',
        r'{"ts":"2023-10-01T10:10:00Z","user":"alice","key":"api_key","val":"***"}',
        r'{"ts":"2023-10-01T10:15:00Z","user":"bob","key":"theme","val":"dark"}',
        r'{"ts":"2023-10-01T10:20:00Z","user":"charlie","key":"greeting","val":"hello world"}'
    ]

    # The output should be sorted alphabetically, so the expected lines are already sorted.
    expected_sorted = sorted(expected_lines)

    actual_lines = content.split("\n") if content else []

    assert len(actual_lines) == len(expected_sorted), f"Expected {len(expected_sorted)} lines in {clean_file}, found {len(actual_lines)}"

    for expected, actual in zip(expected_sorted, actual_lines):
        assert expected == actual, f"Line mismatch in {clean_file}.\nExpected: {expected}\nActual: {actual}"