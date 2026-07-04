# test_final_state.py
import os
import csv

def test_process_go_exists():
    assert os.path.isfile("/home/user/tracker/process.go"), "The file /home/user/tracker/process.go does not exist. Did you create your Go program in the correct location?"

def test_processed_configs_matches_expected():
    expected_file = "/home/user/expected_configs.csv"
    actual_file = "/home/user/processed_configs.csv"

    assert os.path.isfile(actual_file), f"The output file {actual_file} was not created. Ensure your program writes to the correct path."

    with open(expected_file, 'r', newline='', encoding='utf-8') as f:
        expected_rows = [row for row in csv.reader(f) if row]

    with open(actual_file, 'r', newline='', encoding='utf-8') as f:
        actual_rows = [row for row in csv.reader(f) if row]

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in output (including header), but got {len(actual_rows)}."

    for i, (exp, act) in enumerate(zip(expected_rows, actual_rows)):
        assert exp == act, f"Mismatch at row {i+1}.\nExpected: {exp}\nActual:   {act}"