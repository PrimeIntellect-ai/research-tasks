# test_final_state.py

import os
import hashlib
import pytest
from collections import defaultdict

def test_files_exist():
    base_dir = "/home/user/data_pipeline"
    expected_files = [
        "aggregate.c",
        "Makefile",
        "aggregated.csv",
        "reproducibility_report.txt"
    ]
    for filename in expected_files:
        path = os.path.join(base_dir, filename)
        assert os.path.exists(path), f"File {path} is missing."

def test_aggregated_csv_content():
    raw_path = "/home/user/data_pipeline/raw_sensors.csv"
    agg_path = "/home/user/data_pipeline/aggregated.csv"

    assert os.path.exists(raw_path), "raw_sensors.csv is missing."
    assert os.path.exists(agg_path), "aggregated.csv is missing."

    # Compute expected aggregates from raw data
    stats = defaultdict(lambda: {"count": 0, "min": float('inf'), "max": float('-inf'), "sum": 0.0})

    with open(raw_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 3:
                continue

            sensor_id = int(parts[1])
            value = float(parts[2])

            stats[sensor_id]["count"] += 1
            stats[sensor_id]["min"] = min(stats[sensor_id]["min"], value)
            stats[sensor_id]["max"] = max(stats[sensor_id]["max"], value)
            stats[sensor_id]["sum"] += value

    expected_data = {}
    for sid, s in stats.items():
        avg = s["sum"] / s["count"]
        expected_data[sid] = {
            "count": s["count"],
            "min": round(s["min"], 2),
            "max": round(s["max"], 2),
            "avg": round(avg, 2)
        }

    # Read aggregated.csv
    with open(agg_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, "aggregated.csv is empty."
    assert lines[0] == "sensor_id,count,min,max,avg", "Incorrect header in aggregated.csv"

    assert len(lines) - 1 == len(expected_data), "Incorrect number of rows in aggregated.csv"

    for line in lines[1:]:
        parts = line.split(',')
        assert len(parts) == 5, f"Row does not have 5 columns: {line}"
        sid = int(parts[0])
        assert sid in expected_data, f"Unexpected sensor_id: {sid}"

        assert int(parts[1]) == expected_data[sid]["count"], f"Bad count for sensor {sid}"
        assert abs(float(parts[2]) - expected_data[sid]["min"]) < 0.015, f"Bad min for sensor {sid}"
        assert abs(float(parts[3]) - expected_data[sid]["max"]) < 0.015, f"Bad max for sensor {sid}"
        assert abs(float(parts[4]) - expected_data[sid]["avg"]) < 0.015, f"Bad avg for sensor {sid}"

def test_reproducibility_report():
    agg_path = "/home/user/data_pipeline/aggregated.csv"
    report_path = "/home/user/data_pipeline/reproducibility_report.txt"

    assert os.path.exists(agg_path), "aggregated.csv is missing."
    assert os.path.exists(report_path), "reproducibility_report.txt is missing."

    with open(agg_path, "rb") as f:
        true_md5 = hashlib.md5(f.read()).hexdigest()

    with open(report_path, "r") as f:
        report_lines = f.read().strip().split('\n')

    assert len(report_lines) == 4, f"Report should have exactly 4 lines, found {len(report_lines)}"

    assert report_lines[0].startswith("Run 1:"), "Line 1 should start with 'Run 1:'"
    assert true_md5 in report_lines[0], f"Run 1 MD5 mismatch. Expected {true_md5}"

    assert report_lines[1].startswith("Run 2:"), "Line 2 should start with 'Run 2:'"
    assert true_md5 in report_lines[1], f"Run 2 MD5 mismatch. Expected {true_md5}"

    assert report_lines[2].startswith("Run 3:"), "Line 3 should start with 'Run 3:'"
    assert true_md5 in report_lines[2], f"Run 3 MD5 mismatch. Expected {true_md5}"

    assert report_lines[3] == "Reproducible: YES", f"Reproducibility line missing or incorrect. Found: {report_lines[3]}"