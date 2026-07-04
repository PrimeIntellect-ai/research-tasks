# test_final_state.py

import os
import pytest

def test_output_file_exists_and_content():
    output_file = "/home/user/output.csv"

    assert os.path.exists(output_file), f"Missing required output file: {output_file}"
    assert os.path.isfile(output_file), f"Expected {output_file} to be a file, but it is not."

    expected_content = (
        "1700000000,LocátionB,15.50\n"
        "1700000060,LocátionB,15.50\n"
        "1700000120,Tést✓,20.00\n"
        "1700000180,New Data,25.00\n"
    )

    with open(output_file, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # Normalize line endings just in case
    actual_lines = [line.strip() for line in actual_content.strip().split('\n')]
    expected_lines = [line.strip() for line in expected_content.strip().split('\n')]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_file}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {output_file} does not match.\nExpected: {expected}\nActual:   {actual}"