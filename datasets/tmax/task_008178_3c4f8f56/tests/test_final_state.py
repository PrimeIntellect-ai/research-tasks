# test_final_state.py

import os
import csv
import pytest

OUTPUT_CSV = "/home/user/output.csv"

def test_output_file_exists():
    assert os.path.exists(OUTPUT_CSV), f"Output file {OUTPUT_CSV} does not exist."
    assert os.path.isfile(OUTPUT_CSV), f"{OUTPUT_CSV} is not a file."

def test_output_csv_content():
    assert os.path.exists(OUTPUT_CSV), f"Output file {OUTPUT_CSV} missing."

    with open(OUTPUT_CSV, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output CSV is empty."

    header = rows[0]
    expected_header = ["timestamp", "device_id", "temp_c", "humidity_pct", "rolling_temp_c", "high_risk"]
    assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == 8, f"Expected 8 data rows, got {len(data_rows)}."

    # Expected data computed from the rules
    expected_data = [
        ["2023-10-01T10:00:00", "D1", "28.0", "65.0", "28.0", "0"],
        ["2023-10-01T10:01:00", "D1", "29.5", "72.0", "28.75", "0"],
        ["2023-10-01T10:02:00", "D1", "31.0", "75.0", "29.5", "0"],
        ["2023-10-01T10:03:00", "D1", "32.0", "71.0", "30.83", "1"],
        ["2023-10-01T10:04:00", "D1", "33.0", "60.0", "32.0", "0"],
        ["2023-10-01T10:00:00", "D2", "25.0", "80.0", "25.0", "0"],
        ["2023-10-01T10:01:00", "D2", "26.0", "85.0", "25.5", "0"],
        ["2023-10-01T10:02:00", "D2", "27.0", "75.0", "26.0", "0"],
    ]

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        # Compare each field
        assert actual[0] == expected[0], f"Row {i+1}: timestamp mismatch. Expected {expected[0]}, got {actual[0]}."
        assert actual[1] == expected[1], f"Row {i+1}: device_id mismatch. Expected {expected[1]}, got {actual[1]}."
        assert float(actual[2]) == float(expected[2]), f"Row {i+1}: temp_c mismatch. Expected {expected[2]}, got {actual[2]}."
        assert float(actual[3]) == float(expected[3]), f"Row {i+1}: humidity_pct mismatch. Expected {expected[3]}, got {actual[3]}."
        assert float(actual[4]) == float(expected[4]), f"Row {i+1}: rolling_temp_c mismatch. Expected {expected[4]}, got {actual[4]}."
        assert actual[5] == expected[5], f"Row {i+1}: high_risk mismatch. Expected {expected[5]}, got {actual[5]}."