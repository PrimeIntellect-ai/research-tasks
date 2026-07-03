# test_final_state.py
import os
import pytest

def test_processed_sums_log():
    log_path = "/home/user/processed_sums.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. The Go program may not have run or processed files correctly."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {"batch_1.csv:50", "batch_2.csv:95", "batch_3.csv:80"}

    # Check if all expected lines are present (order independent)
    assert set(lines) == expected_lines, f"Log file contents do not match expected sums. Found: {lines}, Expected: {expected_lines}"

def test_incoming_data_empty():
    dir_path = "/home/user/incoming_data/"
    assert os.path.exists(dir_path), f"Directory {dir_path} does not exist."

    # Check if directory is empty of .csv files
    files = os.listdir(dir_path)
    csv_files = [f for f in files if f.endswith('.csv')]
    assert len(csv_files) == 0, f"Directory {dir_path} still contains CSV files, which should have been deleted: {csv_files}"

def test_go_program_exists():
    src_path = "/home/user/aggregator.go"
    bin_path = "/home/user/aggregator"

    assert os.path.exists(src_path), f"Go source file {src_path} does not exist."
    assert os.path.exists(bin_path), f"Go compiled binary {bin_path} does not exist. Did you compile the program?"
    assert os.access(bin_path, os.X_OK), f"Go binary {bin_path} is not executable."