# test_final_state.py

import os
import json
import csv
import re
from datetime import datetime, timedelta

BASE_DIR = "/home/user/sensor_etl"
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "final_metrics.csv")
MAKEFILE = os.path.join(BASE_DIR, "Makefile")

def parse_iso(dt_str):
    return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")

def format_iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def compute_expected_data():
    # 1. Read metadata
    with open(os.path.join(DATA_DIR, "metadata.json"), "r") as f:
        metadata = json.load(f)

    # 2. Read calibrations
    calibrations = []
    calib_pattern = re.compile(r"\[.*?\] (.*?) - Sensor \[(.*?)\] calibrated\. New multiplier: (.*)")
    with open(os.path.join(DATA_DIR, "calibrations.log"), "r") as f:
        for line in f:
            match = calib_pattern.search(line)
            if match:
                ts, sensor, mult = match.groups()
                calibrations.append({
                    "timestamp": parse_iso(ts),
                    "sensor": sensor,
                    "multiplier": float(mult)
                })

    # 3. Read raw readings
    raw_readings = []
    with open(os.path.join(DATA_DIR, "raw_readings.csv"), "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_readings.append({
                "timestamp": parse_iso(row["timestamp"]),
                "sensor": row["sensor_id"],
                "raw_value": float(row["raw_value"])
            })

    # Compute true values
    true_readings = []
    for r in raw_readings:
        sensor = r["sensor"]
        ts = r["timestamp"]
        raw_val = r["raw_value"]

        # Find latest calibration at or before ts
        applicable_calibs = [c for c in calibrations if c["sensor"] == sensor and c["timestamp"] <= ts]
        mult = 1.0
        if applicable_calibs:
            applicable_calibs.sort(key=lambda x: x["timestamp"])
            mult = applicable_calibs[-1]["multiplier"]

        baseline = metadata.get(sensor, {}).get("baseline", 0.0)
        true_val = (raw_val * mult) - baseline
        true_readings.append({
            "timestamp": ts,
            "sensor": sensor,
            "true_value": true_val
        })

    # Resample
    start_time = parse_iso("2023-11-01T10:00:00Z")
    end_time = parse_iso("2023-11-01T10:10:00Z")

    sensors = sorted(list(metadata.keys()))
    resampled = {s: {} for s in sensors}

    curr_time = start_time
    while curr_time <= end_time:
        for s in sensors:
            # Forward fill: find latest reading at or before curr_time
            past_readings = [r for r in true_readings if r["sensor"] == s and r["timestamp"] <= curr_time]
            if past_readings:
                past_readings.sort(key=lambda x: x["timestamp"])
                val = past_readings[-1]["true_value"]
            else:
                val = None
            resampled[s][curr_time] = val
        curr_time += timedelta(minutes=1)

    # Rolling average and format
    expected_rows = []
    curr_time = start_time
    while curr_time <= end_time:
        for s in sensors:
            val = resampled[s][curr_time]

            # 3-min window: curr, curr-1m, curr-2m
            window_vals = []
            for offset in [0, 1, 2]:
                t = curr_time - timedelta(minutes=offset)
                if t in resampled[s] and resampled[s][t] is not None:
                    window_vals.append(resampled[s][t])

            if window_vals:
                avg = sum(window_vals) / len(window_vals)
            else:
                avg = None

            expected_rows.append({
                "timestamp": format_iso(curr_time),
                "sensor_id": s,
                "resampled_true_value": f"{val:.2f}" if val is not None else "",
                "rolling_3min_avg": f"{avg:.2f}" if avg is not None else ""
            })
        curr_time += timedelta(minutes=1)

    return expected_rows

def test_makefile_exists():
    assert os.path.isfile(MAKEFILE), f"Makefile not found at {MAKEFILE}"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

def test_output_content():
    expected_rows = compute_expected_data()

    actual_rows = []
    with open(OUTPUT_FILE, "r") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["timestamp", "sensor_id", "resampled_true_value", "rolling_3min_avg"], \
            "CSV headers do not match the required specification."
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in output, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual["timestamp"] == expected["timestamp"], f"Row {i+1}: expected timestamp {expected['timestamp']}, got {actual['timestamp']}"
        assert actual["sensor_id"] == expected["sensor_id"], f"Row {i+1}: expected sensor_id {expected['sensor_id']}, got {actual['sensor_id']}"
        assert actual["resampled_true_value"] == expected["resampled_true_value"], \
            f"Row {i+1} ({expected['timestamp']} {expected['sensor_id']}): expected resampled_true_value {expected['resampled_true_value']}, got {actual['resampled_true_value']}"
        assert actual["rolling_3min_avg"] == expected["rolling_3min_avg"], \
            f"Row {i+1} ({expected['timestamp']} {expected['sensor_id']}): expected rolling_3min_avg {expected['rolling_3min_avg']}, got {actual['rolling_3min_avg']}"