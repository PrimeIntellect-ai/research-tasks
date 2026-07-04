# test_final_state.py

import os
import csv

def test_cleaned_data_exists():
    """Verify that the cleaned data CSV file was generated in the correct location."""
    file_path = "/home/user/remote_archive/cleaned_data.csv"
    assert os.path.exists(file_path), f"Expected output file not found at {file_path}"
    assert os.path.isfile(file_path), f"Expected {file_path} to be a file, but it is not."

def test_cleaned_data_contents():
    """Verify that the cleaned data CSV contains the correctly processed data."""
    file_path = "/home/user/remote_archive/cleaned_data.csv"
    assert os.path.exists(file_path), f"Cannot verify contents because {file_path} is missing."

    expected_rows = [
        ["timestamp", "sensor_id", "temperature"],
        ["2023-11-01T08:00:00", "sensor_alpha", "20.0"],
        ["2023-11-01T08:00:00", "sensor_beta", "15.5"],
        ["2023-11-01T08:15:00", "sensor_alpha", "22.5"],
        ["2023-11-01T08:15:00", "sensor_beta", "16.0"],
        ["2023-11-01T08:30:00", "sensor_alpha", "25.0"],
        ["2023-11-01T08:30:00", "sensor_beta", "17.0"],
        ["2023-11-01T08:45:00", "sensor_alpha", "24.0"],
        ["2023-11-01T08:45:00", "sensor_beta", "18.0"],
    ]

    actual_rows = []
    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Ignore trailing empty lines if any
                actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), (
        f"Row count mismatch. Expected {len(expected_rows)} rows (including header), "
        f"but got {len(actual_rows)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, (
            f"Row {i} mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )