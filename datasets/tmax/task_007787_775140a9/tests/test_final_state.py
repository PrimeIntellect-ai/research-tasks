# test_final_state.py
import os
import csv
import pytest

HOURLY_SUMMARY_PATH = '/home/user/hourly_summary.csv'
HIGH_RISK_SAMPLE_PATH = '/home/user/high_risk_sample.csv'

def read_csv_as_dicts(file_path):
    assert os.path.exists(file_path), f"File not found: {file_path}"
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_hourly_summary_exists_and_columns():
    """Verify that hourly_summary.csv exists and has the correct columns."""
    data = read_csv_as_dicts(HOURLY_SUMMARY_PATH)
    assert len(data) > 0, "hourly_summary.csv is empty."

    expected_cols = {'timestamp', 'truck_id', 'max_temp', 'avg_speed', 'rolling_3h_max_temp'}
    actual_cols = set(data[0].keys())
    assert expected_cols.issubset(actual_cols), f"Missing columns in hourly_summary.csv. Expected {expected_cols}, got {actual_cols}"

def test_high_risk_sample_exists_and_columns():
    """Verify that high_risk_sample.csv exists and has the correct columns."""
    data = read_csv_as_dicts(HIGH_RISK_SAMPLE_PATH)
    assert len(data) > 0, "high_risk_sample.csv is empty."

    expected_cols = {'timestamp', 'truck_id', 'max_temp', 'avg_speed', 'rolling_3h_max_temp'}
    actual_cols = set(data[0].keys())
    assert expected_cols.issubset(actual_cols), f"Missing columns in high_risk_sample.csv. Expected {expected_cols}, got {actual_cols}"

def test_hourly_summary_computations():
    """Verify specific computed values in hourly_summary.csv for TRUCK_A."""
    data = read_csv_as_dicts(HOURLY_SUMMARY_PATH)

    # Filter and sort TRUCK_A by timestamp
    truck_a_data = [row for row in data if row['truck_id'] == 'TRUCK_A']
    truck_a_data.sort(key=lambda x: x['timestamp'])

    assert len(truck_a_data) >= 4, "Not enough hourly records for TRUCK_A"

    # 8am hour max_temp should be -12.0
    hour_0_max_temp = float(truck_a_data[0]['max_temp'])
    assert abs(hour_0_max_temp - (-12.0)) < 0.01, f"Incorrect max_temp for TRUCK_A hour 0. Expected -12.0, got {hour_0_max_temp}"

    # 10am hour (index 2) rolling_3h_max_temp should be -12.0
    hour_2_rolling = float(truck_a_data[2]['rolling_3h_max_temp'])
    assert abs(hour_2_rolling - (-12.0)) < 0.01, f"Incorrect rolling_3h_max_temp for TRUCK_A at index 2. Expected -12.0, got {hour_2_rolling}"

def test_high_risk_sample_computations():
    """Verify that the high risk sample contains exactly one highest risk record per truck."""
    data = read_csv_as_dicts(HIGH_RISK_SAMPLE_PATH)

    assert len(data) == 2, f"high_risk_sample.csv should have exactly 2 rows (1 per truck), got {len(data)}"

    truck_a_rows = [row for row in data if row['truck_id'] == 'TRUCK_A']
    truck_b_rows = [row for row in data if row['truck_id'] == 'TRUCK_B']

    assert len(truck_a_rows) == 1, "Expected exactly 1 row for TRUCK_A in high_risk_sample.csv"
    assert len(truck_b_rows) == 1, "Expected exactly 1 row for TRUCK_B in high_risk_sample.csv"

    a_max_temp = float(truck_a_rows[0]['max_temp'])
    b_max_temp = float(truck_b_rows[0]['max_temp'])

    assert abs(a_max_temp - (-7.0)) < 0.01, f"Incorrect stratified sample for TRUCK_A. Expected max_temp -7.0, got {a_max_temp}"
    assert abs(b_max_temp - (-9.0)) < 0.01, f"Incorrect stratified sample for TRUCK_B. Expected max_temp -9.0, got {b_max_temp}"