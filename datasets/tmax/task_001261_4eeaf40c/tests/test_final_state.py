# test_final_state.py
import os
import csv
import json
import math
import subprocess

def test_clean_data_csv():
    clean_csv_path = "/home/user/clean_data/sensors_20231001_clean.csv"
    assert os.path.isfile(clean_csv_path), f"Clean data file missing: {clean_csv_path}"

    with open(clean_csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["timestamp", "sensor_id", "value"], "Clean data file has incorrect header."

        rows = list(reader)
        assert len(rows) == 72, f"Expected 72 data rows, got {len(rows)}."

        # Check sorting
        for i in range(len(rows) - 1):
            assert (rows[i][1], rows[i][0]) <= (rows[i+1][1], rows[i+1][0]), "Clean data is not properly sorted by sensor_id, then timestamp."

        # Check deduplication
        seen = set()
        for row in rows:
            record = (row[0], row[1], row[2])
            assert record not in seen, f"Duplicate record found: {record}"
            seen.add(record)

def test_distances_csv():
    distances_csv_path = "/home/user/metrics/distances.csv"
    assert os.path.isfile(distances_csv_path), f"Distances file missing: {distances_csv_path}"

    # Recompute ground truth distances
    clean_csv_path = "/home/user/clean_data/sensors_20231001_clean.csv"
    baseline_path = "/home/user/reference/baseline.json"

    with open(baseline_path, "r") as f:
        baseline = json.load(f)

    sensor_data = {}
    with open(clean_csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor_id = row["sensor_id"]
            if sensor_id not in sensor_data:
                sensor_data[sensor_id] = []
            sensor_data[sensor_id].append(float(row["value"]))

    expected_distances = {}
    for sensor_id, values in sensor_data.items():
        assert len(values) == 24, f"Sensor {sensor_id} does not have exactly 24 readings."
        dist = math.sqrt(sum((v - b) ** 2 for v, b in zip(values, baseline)))
        expected_distances[sensor_id] = f"{dist:.2f}"

    with open(distances_csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["sensor_id", "distance"], "Distances file has incorrect header."

        rows = list(reader)
        assert len(rows) == len(expected_distances), f"Expected {len(expected_distances)} distance rows, got {len(rows)}."

        # Check sorting
        for i in range(len(rows) - 1):
            assert rows[i][0] <= rows[i+1][0], "Distances file is not sorted by sensor_id."

        for row in rows:
            sensor_id, dist = row
            assert sensor_id in expected_distances, f"Unexpected sensor_id: {sensor_id}"
            assert dist == expected_distances[sensor_id], f"Incorrect distance for {sensor_id}: expected {expected_distances[sensor_id]}, got {dist}"

def test_cron_job():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to list crontab."

    crontab_content = result.stdout
    assert "run_pipeline.sh" in crontab_content, "run_pipeline.sh not found in crontab."

    # Check for correct cron schedule "0 0 * * *"
    found = False
    for line in crontab_content.splitlines():
        if "run_pipeline.sh" in line and not line.strip().startswith("#"):
            parts = line.split()
            if len(parts) >= 5 and parts[:5] == ["0", "0", "*", "*", "*"]:
                found = True
                break
    assert found, "Cron job for run_pipeline.sh is not scheduled at exactly '0 0 * * *'."