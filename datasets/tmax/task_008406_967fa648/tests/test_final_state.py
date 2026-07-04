# test_final_state.py

import os
import csv

def test_dataset_extracted():
    """Verify that the dataset was extracted to the correct directory."""
    assert os.path.isdir("/home/user/dataset"), "Directory /home/user/dataset does not exist."
    # Check for a few expected files from the extraction
    assert os.path.isfile("/home/user/dataset/run_A/exp1.log"), "/home/user/dataset/run_A/exp1.log is missing."
    assert os.path.isfile("/home/user/dataset/run_B/exp2.log"), "/home/user/dataset/run_B/exp2.log is missing."

def test_c_program_exists():
    """Verify that the C program was created."""
    assert os.path.isfile("/home/user/parse_dataset.c"), "/home/user/parse_dataset.c does not exist."

def test_results_csv_contents():
    """Verify that the results.csv file contains the correct data in the correct order."""
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    with open(results_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    expected_rows = [
        ["Experiment", "Result"],
        ["EXP-002", "99.1"],
        ["EXP-003", "45.2"],
        ["EXP-004", "12.8"]
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in results.csv, but found {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."