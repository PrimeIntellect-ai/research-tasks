# test_final_state.py
import os
import csv
import glob
import math
import pytest

def get_original_data():
    input_file = "/home/user/sensor_data_wide.csv"
    sensors = {}
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            sensor_id = row[0]
            values = row[1:]
            sensors[sensor_id] = values
    return sensors

def interpolate_values(values):
    # Parse to float or None
    parsed = []
    for v in values:
        if v == 'NaN':
            parsed.append(None)
        else:
            parsed.append(float(v))

    n = len(parsed)
    # Forward/backward fill for edges, linear for middle
    # First, find first valid
    first_valid_idx = 0
    while first_valid_idx < n and parsed[first_valid_idx] is None:
        first_valid_idx += 1

    # If all missing, return (edge case, not in our data)
    if first_valid_idx == n:
        return parsed

    # Fill leading NaNs
    for i in range(first_valid_idx):
        parsed[i] = parsed[first_valid_idx]

    # Find last valid
    last_valid_idx = n - 1
    while last_valid_idx >= 0 and parsed[last_valid_idx] is None:
        last_valid_idx -= 1

    # Fill trailing NaNs
    for i in range(last_valid_idx + 1, n):
        parsed[i] = parsed[last_valid_idx]

    # Fill middle NaNs
    for i in range(first_valid_idx + 1, last_valid_idx):
        if parsed[i] is None:
            # Find next valid
            next_valid_idx = i + 1
            while parsed[next_valid_idx] is None:
                next_valid_idx += 1

            v_start = parsed[i - 1]
            v_end = parsed[next_valid_idx]
            t_start = i - 1
            t_end = next_valid_idx

            # Linear interpolation
            for j in range(i, next_valid_idx):
                parsed[j] = v_start + (v_end - v_start) * (j - t_start) / (t_end - t_start)

    return parsed

def test_cleaned_long_data_exists_and_format():
    output_file = "/home/user/cleaned_long_data.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['sensor_id', 'time_index', 'value'], "Header is incorrect in cleaned_long_data.csv"

        rows = list(reader)
        assert len(rows) == 1000, f"Expected 1000 rows, got {len(rows)}"

def test_cleaned_long_data_values():
    output_file = "/home/user/cleaned_long_data.csv"
    original_data = get_original_data()

    expected_data = {}
    for sensor_id, values in original_data.items():
        expected_data[sensor_id] = interpolate_values(values)

    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header

        for row in reader:
            sensor_id, time_index, value = row
            time_index = int(time_index)
            value = float(value)

            expected_val = expected_data[sensor_id][time_index]
            assert math.isclose(value, expected_val, abs_tol=1e-3), f"Value mismatch for {sensor_id} at t={time_index}: expected {expected_val:.4f}, got {value:.4f}"

def test_reports_exist_and_content():
    reports_dir = "/home/user/reports/"
    assert os.path.isdir(reports_dir), f"Reports directory {reports_dir} does not exist."

    original_data = get_original_data()

    for sensor_id, values in original_data.items():
        report_file = os.path.join(reports_dir, f"sensor_{sensor_id}_report.txt")
        assert os.path.isfile(report_file), f"Report file {report_file} does not exist."

        interpolated = interpolate_values(values)
        avg_val = sum(interpolated) / len(interpolated)
        max_val = max(interpolated)

        # Count NaNs in original
        nan_count = sum(1 for v in values if v == 'NaN')

        with open(report_file, 'r') as f:
            content = f.read()

        assert f"Report for Sensor: {sensor_id}" in content, f"Missing or incorrect sensor ID in {report_file}"
        assert "Total Data Points: 100" in content, f"Missing or incorrect total points in {report_file}"
        assert f"Imputed Points: {nan_count}" in content, f"Missing or incorrect imputed points in {report_file}"

        # Check average and max with some tolerance in string representation
        # The prompt asks for 4 decimal places, so we can check if the rounded string is in the content
        avg_str = f"{avg_val:.4f}"
        max_str = f"{max_val:.4f}"

        # Sometimes float formatting might differ slightly, so we check prefix
        assert avg_str[:-1] in content, f"Expected average value ~{avg_str} in {report_file}"
        assert max_str[:-1] in content, f"Expected max value ~{max_str} in {report_file}"