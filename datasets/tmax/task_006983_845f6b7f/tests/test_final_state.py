# test_final_state.py

import os
import csv

def test_anomalies_csv_exists():
    csv_path = "/home/user/anomalies.csv"
    assert os.path.exists(csv_path), f"The file {csv_path} was not created."
    assert os.path.isfile(csv_path), f"The path {csv_path} is not a file."

def test_anomalies_csv_contents():
    csv_path = "/home/user/anomalies.csv"
    assert os.path.exists(csv_path), f"The file {csv_path} does not exist."

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The anomalies.csv file is empty."

    header = rows[0]
    expected_header = ["timestamp", "endpoint", "response_time_ms", "rolling_avg"]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == 2, f"Expected exactly 2 anomaly rows, but got {len(data_rows)}."

    # Expected anomalies
    expected_rows = [
        ["2023-10-01T10:00:06Z", "/api/users", "450", "102.0"],
        ["2023-10-01T10:00:07Z", "/api/auth", "200", "52.0"]
    ]

    for i, expected in enumerate(expected_rows):
        assert data_rows[i] == expected, f"Row {i+1} mismatch. Expected {expected}, but got {data_rows[i]}."