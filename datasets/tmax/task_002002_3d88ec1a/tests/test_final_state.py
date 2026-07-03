# test_final_state.py

import os
import csv

def test_cpp_source_exists():
    source_path = '/home/user/process_backups.cpp'
    assert os.path.exists(source_path), f"Source file {source_path} does not exist."
    assert os.path.isfile(source_path), f"{source_path} is not a file."

def test_executable_exists():
    exe_path = '/home/user/process_backups'
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.path.isfile(exe_path), f"{exe_path} is not a file."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_csv_output():
    csv_path = '/home/user/backup_plan.csv'
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    expected_rows = [
        ['node_id', 'backup_id', 'size_bytes', 'path_cost'],
        ['1', 'b2', '150', '10'],
        ['2', 'b3', '200', '15'],
        ['3', 'b5', '350', '15'],
        ['4', 'b6', '400', '16']
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."