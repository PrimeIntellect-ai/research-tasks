# test_final_state.py

import os
import csv
import pytest

def test_c_source_exists():
    """Check that the C source file exists."""
    assert os.path.exists("/home/user/process_data.c"), "/home/user/process_data.c does not exist."
    assert os.path.isfile("/home/user/process_data.c"), "/home/user/process_data.c is not a file."

def test_executable_exists():
    """Check that the compiled executable exists and is executable."""
    executable_path = "/home/user/etl_parser"
    assert os.path.exists(executable_path), f"{executable_path} does not exist."
    assert os.path.isfile(executable_path), f"{executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_result_file_correctness():
    """Check that the result file exists and contains the exact expected metrics."""
    data_path = "/home/user/data.csv"
    result_path = "/home/user/etl_result.txt"

    assert os.path.exists(data_path), f"Input data file {data_path} is missing."
    assert os.path.exists(result_path), f"Output result file {result_path} is missing."

    # Compute the expected values
    valid_count = 0
    max_val = -float('inf')
    min_val = float('inf')

    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id", "value"], "Unexpected header in data.csv"

        for row in reader:
            if len(row) < 2:
                continue
            val_str = row[1].strip()
            if val_str == '' or val_str == 'NaN':
                continue
            val = int(val_str)
            valid_count += 1
            if val > max_val: max_val = val
            if val < min_val: min_val = val

    expected_output = (
        f"Valid: {valid_count}\n"
        f"Max: {max_val}\n"
        f"Min: {min_val}\n"
    )

    with open(result_path, 'r') as f:
        actual_output = f.read().strip() + "\n"

    assert actual_output == expected_output, (
        f"Contents of {result_path} do not match the expected output.\n"
        f"Expected:\n{expected_output}\n"
        f"Actual:\n{actual_output}"
    )