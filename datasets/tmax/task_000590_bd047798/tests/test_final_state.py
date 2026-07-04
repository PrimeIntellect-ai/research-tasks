# test_final_state.py

import os
import csv
import pytest

def test_script_exists():
    """Verify that the ETL pipeline script exists."""
    script_path = "/home/user/etl_pipeline.sh"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

def test_cleaned_data_exists():
    """Verify that the cleaned data CSV exists."""
    csv_path = "/home/user/cleaned_data.csv"
    assert os.path.isfile(csv_path), f"Expected file {csv_path} does not exist."

def test_anomalies_exists():
    """Verify that the anomalies CSV exists."""
    csv_path = "/home/user/anomalies.csv"
    assert os.path.isfile(csv_path), f"Expected file {csv_path} does not exist."

def test_cleaned_data_content():
    """Verify the contents of the cleaned data CSV."""
    csv_path = "/home/user/cleaned_data.csv"
    if not os.path.exists(csv_path):
        pytest.fail(f"{csv_path} is missing.")

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Cleaned data CSV is empty."

    header = rows[0]
    expected_header = ["timestamp", "sensor_id", "value", "notes", "norm_value"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 5, f"Expected 5 data rows after deduplication, got {len(data_rows)}"

    # Check specific row values to ensure correct cleaning and normalization
    expected_rows = [
        ["1600000000", "S1", "15.5", "Normal reading", "0.1571"],
        ["1600000005", "S1", "15.5", "Normal reading duplicate", "0.1571"],
        ["1600000010", "S1", "45.0", "Spike detected", "1.0000"],
        ["1600000015", "S2", "10.0", "S2 start", "0.0000"],
        ["1600000020", "S1", "16.0", "Back to normal", "0.1714"]
    ]

    for i, expected in enumerate(expected_rows):
        assert data_rows[i] == expected, f"Row {i+1} mismatch. Expected {expected}, got {data_rows[i]}"

def test_anomalies_content():
    """Verify the contents of the anomalies CSV."""
    csv_path = "/home/user/anomalies.csv"
    if not os.path.exists(csv_path):
        pytest.fail(f"{csv_path} is missing.")

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Anomalies CSV is empty."

    header = rows[0]
    expected_header = ["timestamp", "sensor_id", "distance"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 2, f"Expected 2 anomaly rows, got {len(data_rows)}"

    expected_rows = [
        ["1600000010", "S1", "0.8429"],
        ["1600000020", "S1", "0.8286"]
    ]

    for i, expected in enumerate(expected_rows):
        assert data_rows[i] == expected, f"Anomaly row {i+1} mismatch. Expected {expected}, got {data_rows[i]}"