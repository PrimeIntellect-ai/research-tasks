# test_final_state.py

import os
import pytest

def test_c_source_exists():
    assert os.path.isfile("/home/user/app/processor.c"), "C source file /home/user/app/processor.c does not exist"

def test_executable_exists():
    assert os.path.isfile("/home/user/app/processor"), "Compiled executable /home/user/app/processor does not exist"
    assert os.access("/home/user/app/processor", os.X_OK), "/home/user/app/processor is not executable"

def test_output_csv_exists():
    assert os.path.isfile("/home/user/data/output.csv"), "Output file /home/user/data/output.csv does not exist"

def test_output_matches_expected():
    output_path = "/home/user/data/output.csv"
    expected_path = "/home/user/data/expected_output.csv"

    assert os.path.isfile(output_path), f"{output_path} is missing"
    assert os.path.isfile(expected_path), f"{expected_path} is missing"

    with open(output_path, 'r') as f_out, open(expected_path, 'r') as f_exp:
        out_lines = [line.strip() for line in f_out if line.strip()]
        exp_lines = [line.strip() for line in f_exp if line.strip()]

    assert len(out_lines) > 0, "Output CSV is empty"
    assert out_lines[0] == "bucket_ts,bucket_avg,moving_avg", "Output CSV header is incorrect"

    assert len(out_lines) == len(exp_lines), f"Output CSV has {len(out_lines)} lines, expected {len(exp_lines)}"

    for i, (out_line, exp_line) in enumerate(zip(out_lines, exp_lines)):
        assert out_line == exp_line, f"Mismatch at line {i+1}: expected '{exp_line}', got '{out_line}'"