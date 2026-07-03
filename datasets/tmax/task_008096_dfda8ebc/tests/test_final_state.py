# test_final_state.py

import os
import csv
import json
import stat
from collections import defaultdict

def test_run_pipeline_sh_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Orchestrator script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_pipeline_py_exists():
    script_path = "/home/user/pipeline.py"
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."

def test_output_directory_exists():
    assert os.path.isdir("/home/user/output"), "Output directory /home/user/output does not exist."

def get_expected_data():
    input_file = "/home/user/sensor_data.csv"
    assert os.path.isfile(input_file), f"Input file {input_file} missing."

    invalid_rows = []
    valid_rows = []

    with open(input_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for row in reader:
            try:
                temp = float(row["temperature"])
                hum = float(row["humidity"])
                if -20.0 <= temp <= 60.0 and 0.0 <= hum <= 100.0:
                    valid_rows.append(row)
                else:
                    invalid_rows.append(row)
            except ValueError:
                invalid_rows.append(row)

    # Compute rolling stats
    sensor_history = defaultdict(list)
    rolling_stats = []

    # Sort valid rows by timestamp, preserving original order for identical timestamps
    # Since csv reader reads in order, sorting by timestamp is stable.
    valid_rows.sort(key=lambda x: x["timestamp"])

    for row in valid_rows:
        sid = row["sensor_id"]
        temp = float(row["temperature"])
        hum = float(row["humidity"])

        sensor_history[sid].append((temp, hum))

        # Keep only last 3
        history = sensor_history[sid][-3:]

        temp_mavg = round(sum(x[0] for x in history) / len(history), 2)
        hum_mavg = round(sum(x[1] for x in history) / len(history), 2)

        rolling_stats.append({
            "timestamp": row["timestamp"],
            "sensor_id": sid,
            "temp_mavg": temp_mavg,
            "hum_mavg": hum_mavg
        })

    return header, invalid_rows, rolling_stats

def test_invalid_rows_csv():
    invalid_file = "/home/user/output/invalid_rows.csv"
    assert os.path.isfile(invalid_file), f"Invalid rows file {invalid_file} does not exist."

    expected_header, expected_invalid_rows, _ = get_expected_data()

    with open(invalid_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        actual_header = reader.fieldnames
        actual_invalid_rows = list(reader)

    assert actual_header == expected_header, f"Header in invalid_rows.csv does not match expected. Got: {actual_header}"
    assert actual_invalid_rows == expected_invalid_rows, "Contents of invalid_rows.csv do not match expected invalid rows."

def test_rolling_stats_jsonl():
    stats_file = "/home/user/output/rolling_stats.jsonl"
    assert os.path.isfile(stats_file), f"Rolling stats file {stats_file} does not exist."

    _, _, expected_rolling_stats = get_expected_data()

    actual_rolling_stats = []
    with open(stats_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                actual_rolling_stats.append(json.loads(line))

    assert len(actual_rolling_stats) == len(expected_rolling_stats), f"Expected {len(expected_rolling_stats)} lines in rolling_stats.jsonl, got {len(actual_rolling_stats)}."

    for i, (actual, expected) in enumerate(zip(actual_rolling_stats, expected_rolling_stats)):
        assert actual == expected, f"Mismatch at line {i+1} in rolling_stats.jsonl. Expected {expected}, got {actual}."