# test_final_state.py

import os
import re
import math
import pytest

def test_phase1_token():
    dump_path = "/home/user/dump.bin"
    token_path = "/home/user/token.txt"

    assert os.path.isfile(dump_path), f"File {dump_path} is missing."
    assert os.path.isfile(token_path), f"File {token_path} is missing. Did you save the extracted token?"

    # Extract the true token from the dump
    with open(dump_path, 'rb') as f:
        dump_data = f.read()

    match = re.search(b'RECOVERY_TOKEN_[0-9a-f]+', dump_data)
    assert match is not None, "Could not find RECOVERY_TOKEN_ in dump.bin (test environment issue)"
    expected_token = match.group(0).decode('ascii')

    with open(token_path, 'r') as f:
        actual_token = f.read().strip()

    assert actual_token == expected_token, f"Token in {token_path} is incorrect. Expected {expected_token}, got {actual_token}."

def test_phase2_failing_row():
    data_path = "/home/user/app/data.csv"
    failing_row_path = "/home/user/failing_row.csv"

    assert os.path.isfile(data_path), f"File {data_path} is missing."
    assert os.path.isfile(failing_row_path), f"File {failing_row_path} is missing. Did you save the failing row?"

    # Find the failing row in data.csv (the one with 14.5000000)
    expected_row = None
    with open(data_path, 'r') as f:
        for line in f:
            if "14.5" in line:
                expected_row = line.strip()
                break

    assert expected_row is not None, "Could not find the failing row in data.csv (test environment issue)"

    with open(failing_row_path, 'r') as f:
        actual_row = f.read().strip()

    assert actual_row == expected_row, f"Failing row in {failing_row_path} is incorrect. Expected {expected_row}, got {actual_row}."

def test_phase3_result():
    data_path = "/home/user/app/data.csv"
    result_path = "/home/user/result.txt"

    assert os.path.isfile(data_path), f"File {data_path} is missing."
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did you save the final result?"

    # Compute the expected result
    total = 0.0
    with open(data_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 2:
                val = float(parts[1])
                total += math.sqrt(val)

    expected_result = f"{total:.4f}"

    with open(result_path, 'r') as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, f"Result in {result_path} is incorrect. Expected {expected_result}, got {actual_result}."