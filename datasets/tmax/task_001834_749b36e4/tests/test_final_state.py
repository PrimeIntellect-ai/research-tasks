# test_final_state.py

import os
import csv

def test_integration_results_csv():
    """Test that integration_results.csv exists, has correct columns, and is sorted by sensor_id."""
    file_path = "/home/user/integration_results.csv"
    assert os.path.exists(file_path), f"File not found: {file_path}"
    assert os.path.isfile(file_path), f"Expected a file, but found a directory: {file_path}"

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, f"File is empty: {file_path}"

        expected_columns = ['sensor_id', 'total_area']
        assert header == expected_columns, f"Expected columns {expected_columns}, got {header}"

        rows = list(reader)
        assert len(rows) > 0, "No data rows found in integration_results.csv"

        sensor_ids = [row[0] for row in rows]
        assert sensor_ids == sorted(sensor_ids), "The integration results are not sorted alphabetically by sensor_id"

        # Ensure we have A, B, C
        assert set(sensor_ids) == {'A', 'B', 'C'}, "Expected sensor_ids A, B, C in the results"

def test_max_sensor_txt():
    """Test that max_sensor.txt exists and contains the correct result."""
    file_path = "/home/user/max_sensor.txt"
    assert os.path.exists(file_path), f"File not found: {file_path}"
    assert os.path.isfile(file_path), f"Expected a file, but found a directory: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content, "max_sensor.txt is empty"

    # Expected content starts with 'B,25.0' or 'B,25.1'
    assert content.startswith("B,25.0") or content.startswith("B,25.1"), \
        f"Expected max_sensor.txt to start with 'B,25.0' or 'B,25.1', but got '{content}'"