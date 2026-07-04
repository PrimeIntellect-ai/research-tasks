# test_final_state.py
import os
import csv

def test_results_csv_exists():
    """Test that the results.csv file exists in the correct directory."""
    file_path = "/home/user/results.csv"
    assert os.path.exists(file_path), f"Missing file: {file_path}"
    assert os.path.isfile(file_path), f"Not a file: {file_path}"

def test_results_csv_columns():
    """Test that results.csv has the exact expected columns."""
    file_path = "/home/user/results.csv"
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        expected_cols = ['original_message', 'svd_1', 'svd_2', 'is_anomaly']
        assert header == expected_cols, f"Expected columns {expected_cols}, got {header}"

def test_results_csv_content():
    """Test that results.csv is correctly formatted, sorted, and has the right anomaly count."""
    file_path = "/home/user/results.csv"
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 50, f"Expected 50 rows of data, got {len(rows)}"

    # Check that original_message is sorted alphabetically
    messages = [row['original_message'] for row in rows]
    assert messages == sorted(messages), "Error: DataFrame is not sorted alphabetically by original_message."

    # Check is_anomaly values and count
    anomalies_count = 0
    for i, row in enumerate(rows):
        val = row['is_anomaly']
        assert val in ('0', '1'), f"Row {i+1}: is_anomaly column must contain only 0 and 1, got {val}"
        anomalies_count += int(val)

    assert anomalies_count == 5, f"Error: Expected exactly 5 anomalies (10% of 50), found {anomalies_count}"