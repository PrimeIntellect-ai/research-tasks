# test_final_state.py

import os
import csv
import math
from collections import defaultdict

LOG_FILE_PATH = "/home/user/server.log"
C_SOURCE_PATH = "/home/user/analyze_logs.c"
EXECUTABLE_PATH = "/home/user/analyze_logs"
SUMMARY_CSV_PATH = "/home/user/summary.csv"

def test_c_source_exists():
    assert os.path.exists(C_SOURCE_PATH), f"C source file missing at {C_SOURCE_PATH}"
    assert os.path.isfile(C_SOURCE_PATH), f"{C_SOURCE_PATH} is not a file"

def test_executable_exists():
    assert os.path.exists(EXECUTABLE_PATH), f"Compiled executable missing at {EXECUTABLE_PATH}"
    assert os.path.isfile(EXECUTABLE_PATH), f"{EXECUTABLE_PATH} is not a file"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"{EXECUTABLE_PATH} is not executable"

def test_summary_csv_exists():
    assert os.path.exists(SUMMARY_CSV_PATH), f"Summary CSV missing at {SUMMARY_CSV_PATH}"
    assert os.path.isfile(SUMMARY_CSV_PATH), f"{SUMMARY_CSV_PATH} is not a file"

def test_summary_csv_content():
    # Compute expected results from the log file
    assert os.path.exists(LOG_FILE_PATH), f"Log file missing at {LOG_FILE_PATH}"

    aggregations = defaultdict(lambda: {"count": 0, "total_duration": 0, "max_duration": -1})

    with open(LOG_FILE_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(" | ")]
            if len(parts) != 5:
                continue

            timestamp, ip, level, duration_str, endpoint = parts

            # Filtering rules
            if level not in ("INFO", "WARN", "ERROR"):
                continue

            try:
                duration = int(duration_str)
            except ValueError:
                continue

            if duration <= 0:
                continue

            if not endpoint.startswith("/api/"):
                continue

            # Time-based bucketing
            hour_bucket = timestamp[:13]

            # Aggregation
            key = (hour_bucket, endpoint)
            aggregations[key]["count"] += 1
            aggregations[key]["total_duration"] += duration
            if duration > aggregations[key]["max_duration"]:
                aggregations[key]["max_duration"] = duration

    expected_rows = []
    for (hour_bucket, endpoint), stats in aggregations.items():
        avg_duration = math.floor(stats["total_duration"] / stats["count"])
        expected_rows.append({
            "hour_bucket": hour_bucket,
            "endpoint": endpoint,
            "count": str(stats["count"]),
            "avg_duration": str(avg_duration),
            "max_duration": str(stats["max_duration"])
        })

    expected_rows.sort(key=lambda x: (x["hour_bucket"], x["endpoint"]))

    # Read actual results
    actual_rows = []
    with open(SUMMARY_CSV_PATH, 'r', newline='') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["hour_bucket", "endpoint", "count", "avg_duration", "max_duration"], \
            f"CSV header is incorrect. Got: {reader.fieldnames}"
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in CSV, but got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, \
            f"Row {i+1} mismatch.\nExpected: {expected}\nActual: {actual}"