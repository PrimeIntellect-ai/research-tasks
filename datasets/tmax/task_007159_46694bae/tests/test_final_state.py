# test_final_state.py

import os
import csv
import pytest

def test_processed_data_exists():
    file_path = "/home/user/processed_data.csv"
    assert os.path.isfile(file_path), f"The output file {file_path} does not exist."

def test_processed_data_utf8_encoding():
    file_path = "/home/user/processed_data.csv"
    assert os.path.isfile(file_path), f"The output file {file_path} does not exist."
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError:
        pytest.fail(f"The file {file_path} is not valid UTF-8.")

def test_processed_data_contents():
    file_path = "/home/user/processed_data.csv"
    assert os.path.isfile(file_path), f"The output file {file_path} does not exist."

    expected_rows = [
        ['id', 'timestamp', 'log_message', 'temperature', 'rolling_avg'],
        ['1', '2023-10-01T10:00:00', 'User [REDACTED_EMAIL] connected', '20.00', '20.00'],
        ['2', '2023-10-01T10:01:00', 'Café machine active [REDACTED_EMAIL]', '20.00', '20.00'],
        ['3', '2023-10-01T10:02:00', 'Normal operation', '22.00', '20.67'],
        ['4', '2023-10-01T10:03:00', 'Alert sent to [REDACTED_EMAIL]', '22.00', '21.33'],
        ['5', '2023-10-01T10:04:00', 'Shutdown initiated by [REDACTED_EMAIL]', '25.00', '23.00']
    ]

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        assert actual == expected, f"Row {i} mismatch. Expected: {expected}, but got: {actual}"