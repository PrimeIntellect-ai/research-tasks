# test_final_state.py

import os
import csv

def test_calc_token_exists():
    path = "/home/user/.calc_token"
    assert os.path.exists(path), f"The required hidden file {path} was not created."

def test_process_py_exists():
    path = "/home/user/process.py"
    assert os.path.isfile(path), f"The Python script {path} was not created."

def test_final_csv_correct():
    input_path = "/home/user/input.csv"
    final_path = "/home/user/final.csv"

    assert os.path.isfile(final_path), f"The final output file {final_path} was not created."

    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        input_rows = list(reader)

    assert len(input_rows) > 1, f"{input_path} is empty or missing data."
    header = input_rows[0]
    assert header == ['x'], f"Unexpected header in {input_path}."

    expected_rows = [['x', 'y']]
    for row in input_rows[1:]:
        x = int(row[0].strip())
        y = 3 * (x ** 2) + 2 * x + 1
        expected_rows.append([str(x), str(y)])

    with open(final_path, 'r') as f:
        reader = csv.reader(f)
        final_rows = list(reader)

    assert len(final_rows) == len(expected_rows), f"{final_path} does not have the expected number of rows."

    for i, (expected, actual) in enumerate(zip(expected_rows, final_rows)):
        assert actual == expected, f"Row {i+1} in {final_path} is incorrect. Expected {expected}, got {actual}."

def test_output_csv_exists():
    path = "/home/user/output.csv"
    assert os.path.isfile(path), f"The intermediate file {path} was not generated. Did you run legacy_bin?"