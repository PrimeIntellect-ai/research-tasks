# test_final_state.py

import os
import csv
import pytest

def test_go_file_exists():
    go_file = "/home/user/generate_data.go"
    assert os.path.exists(go_file), f"The Go source file {go_file} does not exist."
    assert os.path.isfile(go_file), f"The path {go_file} is not a file."

def test_csv_file_exists_and_valid():
    csv_file = "/home/user/training_data.csv"
    assert os.path.exists(csv_file), f"The output CSV file {csv_file} does not exist."
    assert os.path.isfile(csv_file), f"The path {csv_file} is not a file."

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("The CSV file is empty.")

        expected_header = ['time', 'node0', 'node1', 'node2', 'node3']
        assert header == expected_header, f"Header is incorrect. Expected {expected_header}, got {header}"

        rows = list(reader)

    num_rows = len(rows)
    assert num_rows in [1000, 1001], f"Expected 1000 or 1001 data rows, got {num_rows}."

    # Validate initial state
    try:
        first_row = [float(x) for x in rows[0]]
    except ValueError:
        pytest.fail("First row contains non-numeric values.")

    assert abs(first_row[0] - 0.0) < 1e-4, f"Initial time should be 0.0, got {first_row[0]}"
    assert abs(first_row[1] - 10.0) < 1e-4, f"Initial node0 should be 10.0, got {first_row[1]}"
    assert abs(first_row[2] - 0.0) < 1e-4, f"Initial node1 should be 0.0, got {first_row[2]}"
    assert abs(first_row[3] - 0.0) < 1e-4, f"Initial node2 should be 0.0, got {first_row[3]}"
    assert abs(first_row[4] - 0.0) < 1e-4, f"Initial node3 should be 0.0, got {first_row[4]}"

    # Validate second step mechanics
    try:
        second_row = [float(x) for x in rows[1]]
    except ValueError:
        pytest.fail("Second row contains non-numeric values.")

    assert abs(second_row[1] - 9.8) < 1e-3, f"Step 1 node0 should be ~9.8, got {second_row[1]}"
    assert abs(second_row[2] - 0.1) < 1e-3, f"Step 1 node1 should be ~0.1, got {second_row[2]}"
    assert abs(second_row[3] - 0.0) < 1e-3, f"Step 1 node2 should be ~0.0, got {second_row[3]}"
    assert abs(second_row[4] - 0.1) < 1e-3, f"Step 1 node3 should be ~0.1, got {second_row[4]}"

    # Validate final state (steady state convergence)
    try:
        last_row = [float(x) for x in rows[-1]]
    except ValueError:
        pytest.fail("Last row contains non-numeric values.")

    for i in range(1, 5):
        assert abs(last_row[i] - 2.5) <= 0.1, f"Node {i-1} did not converge to ~2.5, got {last_row[i]}"

    # Check 4 decimal places format
    for val in rows[0]:
        if '.' in val:
            decimals = len(val.split('.')[1])
            assert decimals == 4, f"Values must be formatted to 4 decimal places, got '{val}'"