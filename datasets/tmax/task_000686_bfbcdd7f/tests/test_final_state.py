# test_final_state.py

import os
import csv

def test_cpp_source_exists():
    path = "/home/user/analyze_logs.cpp"
    assert os.path.isfile(path), f"Missing C++ source file: {path}"

def test_anomalies_csv():
    path = "/home/user/anomalies.csv"
    assert os.path.isfile(path), f"Missing output file: {path}"

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The anomalies.csv file is empty."

    header = rows[0]
    expected_header = ["timestamp_a", "X_a", "Y_a", "timestamp_b", "X_b", "Y_b", "distance"]
    assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

    # Expected data rows based on the setup logs
    expected_rows = [
        ["2023-10-25 14:22:02.500", "15.00", "5.00", "2023-10-25 14:22:02.550", "12.00", "2.00", "4.24"],
        ["2023-10-25 14:22:04.900", "0.00", "0.00", "2023-10-25 14:22:04.990", "3.00", "4.00", "5.00"]
    ]

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} anomaly rows, found {len(data_rows)}"

    for i, (actual, expected) in enumerate(zip(data_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}"