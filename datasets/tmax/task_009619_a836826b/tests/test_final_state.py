# test_final_state.py

import os
import pytest

def test_c_source_exists():
    path = "/home/user/src/etl_pipeline.c"
    assert os.path.isfile(path), f"C source file {path} does not exist. Did you create it?"

def test_output_csv_exists_and_correct():
    path = "/home/user/output/normalized_dataset.csv"
    assert os.path.isfile(path), f"Output CSV {path} does not exist. Did you compile and run your program?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "id,token,e0,e1,e2,e3",
        "0,tok_alpha,0.600000,0.000000,0.800000,0.000000",
        "2,tok_gamma,0.000000,0.800000,0.600000,0.000000"
    ]
    expected_content = "\n".join(expected_lines)

    # Compare line by line to give a clear error message
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in CSV does not match expected.\nExpected: {expected}\nActual:   {actual}"