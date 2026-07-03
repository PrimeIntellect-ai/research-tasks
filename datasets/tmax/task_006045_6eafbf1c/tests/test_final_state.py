# test_final_state.py

import os
import csv
import math
import pytest
from datetime import datetime

OUTPUT_FILE = "/home/user/cleaned_sensor_stats.csv"

def read_csv_data(filepath):
    assert os.path.exists(filepath), f"Output file {filepath} not found."
    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = list(reader)
    return header, rows

def parse_float(val):
    val = val.strip()
    if not val:
        return None
    return float(val)

def test_output_file_exists_and_header():
    """Test that the output file exists and has the correct header."""
    header, _ = read_csv_data(OUTPUT_FILE)
    expected_header = ['sensor_id', 'timestamp', 'temperature', 'rolling_avg_temp']
    assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

def test_output_row_count():
    """Test that the output file has exactly 17 data rows."""
    _, rows = read_csv_data(OUTPUT_FILE)
    assert len(rows) == 17, f"Row count mismatch. Expected 17, got {len(rows)}"

def test_output_sorting_and_format():
    """Test that the data is sorted by sensor_id and timestamp, and timestamp is formatted correctly."""
    _, rows = read_csv_data(OUTPUT_FILE)

    prev_sensor = None
    prev_time = None

    for row in rows:
        assert len(row) == 4, f"Row has incorrect number of columns: {row}"
        sensor_id, ts_str, _, _ = row

        try:
            ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pytest.fail(f"Timestamp format incorrect: {ts_str}")

        if prev_sensor is not None:
            if sensor_id == prev_sensor:
                assert ts > prev_time, f"Timestamps not sorted ascending for sensor {sensor_id}: {prev_time} -> {ts}"
            else:
                assert sensor_id > prev_sensor, f"Sensor IDs not sorted ascending: {prev_sensor} -> {sensor_id}"

        prev_sensor = sensor_id
        prev_time = ts

def test_s1_imputation_and_rolling_avg_at_14():
    """Validate specific values for S1 at 14:00 (interpolated and rolling avg)."""
    _, rows = read_csv_data(OUTPUT_FILE)

    s1_14_row = None
    for row in rows:
        if row[0] == 'S1' and row[1] == '2023-10-01 14:00:00':
            s1_14_row = row
            break

    assert s1_14_row is not None, "Row for S1 at 14:00 not found."

    temp = parse_float(s1_14_row[2])
    rolling = parse_float(s1_14_row[3])

    assert temp is not None and math.isclose(temp, 24.0, abs_tol=0.01), f"Imputation error S1 14:00. Expected 24.0, got {temp}"
    assert rolling is not None and math.isclose(rolling, 22.5, abs_tol=0.01), f"Rolling avg error S1 14:00. Expected 22.5, got {rolling}"

def test_s1_missing_gaps_limit_at_15():
    """Validate missing gaps limit (S1 at 15:00 should be NaN, but rolling avg should exist)."""
    _, rows = read_csv_data(OUTPUT_FILE)

    s1_15_row = None
    for row in rows:
        if row[0] == 'S1' and row[1] == '2023-10-01 15:00:00':
            s1_15_row = row
            break

    assert s1_15_row is not None, "Row for S1 at 15:00 not found."

    temp = parse_float(s1_15_row[2])
    rolling = parse_float(s1_15_row[3])

    assert temp is None, f"Interpolation limit not respected for S1 15:00. Expected empty/NaN, got {temp}"
    assert rolling is not None and math.isclose(rolling, 23.0, abs_tol=0.01), f"Rolling avg error over NaNs S1 15:00. Expected 23.0, got {rolling}"

def test_s2_values():
    """Validate a specific row for S2 to ensure correct processing of another group."""
    _, rows = read_csv_data(OUTPUT_FILE)

    s2_14_row = None
    for row in rows:
        if row[0] == 'S2' and row[1] == '2023-10-01 14:00:00':
            s2_14_row = row
            break

    assert s2_14_row is not None, "Row for S2 at 14:00 not found."

    temp = parse_float(s2_14_row[2])
    rolling = parse_float(s2_14_row[3])

    assert temp is not None and math.isclose(temp, 22.0, abs_tol=0.01), f"Temperature error S2 14:00. Expected 22.0, got {temp}"
    assert rolling is not None and math.isclose(rolling, 19.0, abs_tol=0.01), f"Rolling avg error S2 14:00. Expected 19.0, got {rolling}"