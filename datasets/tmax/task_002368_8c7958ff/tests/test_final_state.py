# test_final_state.py
import os
import pytest

def test_c_source_exists():
    assert os.path.isfile('/home/user/graph_optimizer.c'), "The C source file /home/user/graph_optimizer.c is missing."

def test_binary_exists():
    assert os.path.isfile('/home/user/graph_optimizer'), "The compiled binary /home/user/graph_optimizer is missing."
    assert os.access('/home/user/graph_optimizer', os.X_OK), "The file /home/user/graph_optimizer is not executable."

def test_result_file_exists():
    assert os.path.isfile('/home/user/result.csv'), "The output file /home/user/result.csv is missing."

def test_result_matches_expected():
    expected_file = '/home/user/expected_result.csv'
    actual_file = '/home/user/result.csv'

    assert os.path.isfile(expected_file), f"Expected result file {expected_file} is missing from setup."
    assert os.path.isfile(actual_file), f"Actual result file {actual_file} is missing."

    with open(expected_file, 'r') as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    with open(actual_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in result.csv, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1}: expected '{expected}', got '{actual}'."