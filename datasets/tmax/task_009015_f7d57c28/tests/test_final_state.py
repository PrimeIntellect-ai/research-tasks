# test_final_state.py
import os
import csv
import pytest
from datetime import datetime, timezone

def parse_timestamp(ts_str):
    # Try parsing common ISO 8601 formats
    ts_str = ts_str.strip()
    if ts_str.endswith('Z'):
        ts_str = ts_str[:-1] + '+00:00'
    try:
        dt = datetime.fromisoformat(ts_str)
        if dt.tzinfo is None:
            # If naive, assume UTC as per instructions that it might be naive UTC
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt
    except ValueError:
        pytest.fail(f"Invalid timestamp format: {ts_str}")

def test_processed_traffic_csv():
    file_path = '/home/user/processed_traffic.csv'
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    expected_data = [
        ('A', '2023-10-01T10:00:00+00:00', 10, 10.0),
        ('A', '2023-10-01T11:00:00+00:00', 15, 12.5),
        ('A', '2023-10-01T12:00:00+00:00', 20, 17.5),
        ('A', '2023-10-01T13:00:00+00:00', 30, 25.0),
        ('B', '2023-10-01T10:00:00+00:00', 50, 50.0),
        ('B', '2023-10-01T11:00:00+00:00', 60, 55.0),
        ('B', '2023-10-01T12:00:00+00:00', 70, 65.0),
        ('C', '2023-10-01T15:00:00+00:00', 100, 100.0),
        ('C', '2023-10-01T15:30:00+00:00', 120, 110.0),
    ]

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers is not None, "CSV file is empty."

        # Handle optional index column from pandas
        if headers[0] == '' and len(headers) == 5:
            headers = headers[1:]
            has_index = True
        else:
            has_index = False

        expected_headers = ['sensor_id', 'timestamp', 'vehicle_count', 'rolling_avg_2h']
        assert headers == expected_headers, f"Expected headers {expected_headers}, got {headers}"

        rows = list(reader)

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows, found {len(rows)}."

    for i, (row, expected) in enumerate(zip(rows, expected_data)):
        if has_index:
            row = row[1:]

        sensor_id, ts_str, v_count_str, roll_avg_str = row
        exp_sensor, exp_ts_str, exp_v_count, exp_roll_avg = expected

        assert sensor_id == exp_sensor, f"Row {i+1}: expected sensor_id {exp_sensor}, got {sensor_id}"

        dt = parse_timestamp(ts_str)
        exp_dt = parse_timestamp(exp_ts_str)
        assert dt == exp_dt, f"Row {i+1}: expected timestamp {exp_dt}, got {dt}"

        try:
            v_count = int(v_count_str)
        except ValueError:
            pytest.fail(f"Row {i+1}: invalid vehicle_count {v_count_str}")
        assert v_count == exp_v_count, f"Row {i+1}: expected vehicle_count {exp_v_count}, got {v_count}"

        try:
            roll_avg = float(roll_avg_str)
        except ValueError:
            pytest.fail(f"Row {i+1}: invalid rolling_avg_2h {roll_avg_str}")
        assert abs(roll_avg - exp_roll_avg) < 1e-5, f"Row {i+1}: expected rolling_avg_2h {exp_roll_avg}, got {roll_avg}"