# test_final_state.py
import os
import csv

def test_anomalies_csv_exists():
    output_file = "/home/user/anomalies.csv"
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist."

def test_anomalies_csv_content():
    output_file = "/home/user/anomalies.csv"
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist."

    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"File {output_file} is empty."

    header = rows[0]
    expected_header = ["hour", "count", "rolling_avg"]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}"

    # Based on the setup script, the only anomaly is at 2023-10-01T12
    # with count 30 and rolling average 10.0.
    expected_rows = [
        ["2023-10-01T12", "30", "10.0"]
    ]

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(data_rows)}"

    for expected, actual in zip(expected_rows, data_rows):
        assert actual == expected, f"Expected row {expected}, but got {actual}"