# test_final_state.py

import os
import json
import csv
import pytest
from collections import defaultdict

def compute_expected_results(input_file):
    data = defaultdict(lambda: defaultdict(list))

    with open(input_file, "r") as f:
        for line in f:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                # Skip invalid JSON (malformed unicode escapes, etc.)
                continue

            device = record.get("device")
            ts = record.get("ts")
            val = record.get("val")

            if not device or not ts or val is None:
                continue

            # Truncate timestamp to the start of the hour
            # Assumes format like 2023-10-15T14:35:12Z
            hour = ts[:14] + "00:00Z"
            data[device][hour].append(val)

    expected_rows = []

    for device in sorted(data.keys()):
        hours = sorted(data[device].keys())
        hourly_avgs = []
        for i, hour in enumerate(hours):
            avg = sum(data[device][hour]) / len(data[device][hour])
            hourly_avgs.append(avg)

            # Rolling 3-hour average of the calculated hourly averages
            start_idx = max(0, i - 2)
            window = hourly_avgs[start_idx:i+1]
            rolling_avg = sum(window) / len(window)

            expected_rows.append({
                "device": device,
                "hour": hour,
                "hourly_avg": f"{avg:.2f}",
                "rolling_3_avg": f"{rolling_avg:.2f}"
            })

    return expected_rows

def test_script_exists_and_executable():
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_output_csv_exists():
    output_path = "/home/user/rolling_stats.csv"
    assert os.path.isfile(output_path), f"The output CSV {output_path} was not created."

def test_output_csv_content():
    input_path = "/home/user/data/telemetry.jsonl"
    output_path = "/home/user/rolling_stats.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    expected_data = compute_expected_results(input_path)

    actual_data = []
    with open(output_path, "r") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["device", "hour", "hourly_avg", "rolling_3_avg"], \
            f"CSV headers are incorrect. Expected ['device', 'hour', 'hourly_avg', 'rolling_3_avg'], got {reader.fieldnames}"

        for row in reader:
            actual_data.append(row)

    assert len(actual_data) == len(expected_data), \
        f"Row count mismatch. Expected {len(expected_data)} rows, got {len(actual_data)} rows."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual["device"] == expected["device"], f"Row {i+1}: device mismatch. Expected {expected['device']}, got {actual['device']}"
        assert actual["hour"] == expected["hour"], f"Row {i+1}: hour mismatch. Expected {expected['hour']}, got {actual['hour']}"

        # Compare numeric values as floats to avoid strict string formatting issues, though string matching to 2 decimal places is preferred
        actual_hourly = float(actual["hourly_avg"])
        expected_hourly = float(expected["hourly_avg"])
        assert abs(actual_hourly - expected_hourly) < 0.015, \
            f"Row {i+1}: hourly_avg mismatch. Expected {expected['hourly_avg']}, got {actual['hourly_avg']}"

        actual_rolling = float(actual["rolling_3_avg"])
        expected_rolling = float(expected["rolling_3_avg"])
        assert abs(actual_rolling - expected_rolling) < 0.015, \
            f"Row {i+1}: rolling_3_avg mismatch. Expected {expected['rolling_3_avg']}, got {actual['rolling_3_avg']}"