# test_final_state.py

import os
import json
import sqlite3
import statistics
import pytest

def test_unified_logs_exists_and_sorted():
    unified_logs_path = "/home/user/unified_logs.txt"
    assert os.path.exists(unified_logs_path), f"{unified_logs_path} is missing."

    with open(unified_logs_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"{unified_logs_path} is empty."

    # Check formatting and sorting
    timestamps = []
    for line in lines:
        parts = line.split("]", 1)
        assert len(parts) == 2, f"Line format incorrect, missing ']': {line.strip()}"
        assert parts[0].startswith("["), f"Line format incorrect, missing '[': {line.strip()}"

        ts_str = parts[0][1:]
        # Basic ISO8601 length check
        assert len(ts_str) == 20 and ts_str.endswith("Z"), f"Timestamp not in correct ISO8601 format: {ts_str}"
        timestamps.append(ts_str)

    # Check if timestamps are sorted
    assert timestamps == sorted(timestamps), "The entries in unified_logs.txt are not sorted chronologically."

    # Check if the FATAL log is present and is the last one based on the setup
    assert "FATAL" in lines[-1], "The last log entry does not contain 'FATAL'."
    assert "2023-10-25T13:22:05Z" in lines[-1], "The last log entry does not have the correct crash timestamp."

def test_report_json_exists_and_correct():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"{report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not a valid JSON file.")

    assert "crash_time" in data, "Key 'crash_time' missing in report.json"
    assert "anomalous_sensor" in data, "Key 'anomalous_sensor' missing in report.json"
    assert "highest_stddev" in data, "Key 'highest_stddev' missing in report.json"

    # Check crash_time
    assert data["crash_time"] == "2023-10-25T13:22:05Z", f"Incorrect crash_time: {data['crash_time']}"

    # Recompute the truth from the database to be robust
    db_path = "/home/user/data/sensors.db"
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sensor_id, value FROM readings")
    rows = cursor.fetchall()
    conn.close()

    sensor_values = {}
    for sensor_id, value in rows:
        sensor_values.setdefault(sensor_id, []).append(value)

    stddevs = {s: statistics.stdev(vals) for s, vals in sensor_values.items() if len(vals) > 1}

    expected_anomalous_sensor = max(stddevs, key=stddevs.get)
    expected_highest_stddev = round(stddevs[expected_anomalous_sensor], 2)

    assert data["anomalous_sensor"] == expected_anomalous_sensor, f"Incorrect anomalous_sensor: {data['anomalous_sensor']}"

    # Check highest_stddev with some tolerance or exact match to rounded value
    reported_stddev = data["highest_stddev"]
    assert isinstance(reported_stddev, (int, float)), "highest_stddev must be a float."
    assert abs(reported_stddev - expected_highest_stddev) <= 0.1, f"Incorrect highest_stddev: expected approx {expected_highest_stddev}, got {reported_stddev}"