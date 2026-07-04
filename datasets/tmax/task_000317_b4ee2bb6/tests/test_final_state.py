# test_final_state.py

import os

def test_c_file_exists():
    c_path = '/home/user/process_logs.c'
    assert os.path.exists(c_path), f"Source file {c_path} is missing. Did you write the C program?"
    assert os.path.isfile(c_path), f"{c_path} is not a file."

def test_executable_exists():
    exe_path = '/home/user/process_logs'
    assert os.path.exists(exe_path), f"Executable {exe_path} is missing. Did you compile the C program?"
    assert os.path.isfile(exe_path), f"{exe_path} is not a file."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_output_csv_exists():
    out_path = '/home/user/aggregated_metrics.csv'
    assert os.path.exists(out_path), f"Output file {out_path} is missing."
    assert os.path.isfile(out_path), f"{out_path} is not a file."

def test_output_csv_content():
    out_path = '/home/user/aggregated_metrics.csv'
    truth_path = '/home/user/expected_aggregated.csv'

    assert os.path.exists(out_path), f"Output file {out_path} is missing."
    assert os.path.exists(truth_path), f"Truth file {truth_path} is missing."

    with open(out_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    with open(truth_path, 'r') as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Output file has {len(actual_lines)} lines, but expected {len(expected_lines)} lines."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )