# test_final_state.py

import os
import csv
import json
import subprocess
import pytest

def get_expected_crashes():
    processor_log = "/home/user/ingestion_system/logs/processor.log"
    service_a_log = "/home/user/ingestion_system/logs/service_a.log"
    raw_data_file = "/home/user/ingestion_system/raw_data/dump_20231001.jsonl"

    # 1. Find req_ids that crashed
    crash_req_ids = []
    if os.path.exists(processor_log):
        with open(processor_log, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Panic: unwrap()" in line:
                    # Look back for the "Starting processing" line
                    for j in range(i-1, -1, -1):
                        if "Starting processing for" in lines[j]:
                            req_id = lines[j].strip().split()[-1]
                            crash_req_ids.append(req_id)
                            break

    # 2. Get timestamps from service_a.log
    req_to_ts = {}
    if os.path.exists(service_a_log):
        with open(service_a_log, "r") as f:
            for line in f:
                if "Received incoming API request" in line:
                    parts = line.split("INFO: Received incoming API request ")
                    if len(parts) == 2:
                        ts_part = parts[0].strip()[1:-1] # Remove brackets
                        req_id = parts[1].split()[0]
                        req_to_ts[req_id] = ts_part

    # 3. Get payload details from raw_data
    req_to_payload = {}
    if os.path.exists(raw_data_file):
        with open(raw_data_file, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    req_to_payload[data["req_id"]] = data
                except json.JSONDecodeError:
                    pass

    expected_rows = []
    for req_id in crash_req_ids:
        ts = req_to_ts.get(req_id, "")
        payload = req_to_payload.get(req_id, {})
        client_version = payload.get("client_version", "")
        duration = payload.get("metrics", {}).get("duration", "")
        expected_rows.append({
            "timestamp": ts,
            "req_id": req_id,
            "client_version": client_version,
            "duration": str(duration)
        })

    # Sort chronologically
    expected_rows.sort(key=lambda x: x["timestamp"])
    return expected_rows

def test_crash_timeline_csv():
    csv_path = "/home/user/crash_timeline.csv"
    assert os.path.isfile(csv_path), f"{csv_path} does not exist."

    expected_rows = get_expected_crashes()
    assert len(expected_rows) > 0, "Could not determine expected crashes from logs. Environment may be broken."

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)

    assert reader.fieldnames == ["timestamp", "req_id", "client_version", "duration"], \
        f"CSV header is incorrect. Expected ['timestamp', 'req_id', 'client_version', 'duration'], got {reader.fieldnames}"

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in CSV, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual["timestamp"] == expected["timestamp"], f"Row {i+1} timestamp mismatch: expected {expected['timestamp']}, got {actual['timestamp']}"
        assert actual["req_id"] == expected["req_id"], f"Row {i+1} req_id mismatch: expected {expected['req_id']}, got {actual['req_id']}"
        assert actual["client_version"] == expected["client_version"], f"Row {i+1} client_version mismatch: expected {expected['client_version']}, got {actual['client_version']}"
        assert int(actual["duration"]) < 0, f"Row {i+1} duration must be negative, got {actual['duration']}"
        assert actual["duration"] == expected["duration"], f"Row {i+1} duration mismatch: expected {expected['duration']}, got {actual['duration']}"

def test_regression_test_script():
    script_path = "/home/user/regression_test.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the regression test
    result = subprocess.run([script_path], capture_output=True, text=True)

    assert result.returncode == 0, f"Regression test script failed with exit code {result.returncode}. Output: {result.stdout}\n{result.stderr}"
    assert "Test Passed: Crash Reproduced" in result.stdout or "Test Passed" in result.stdout, \
        f"Regression test did not output the expected success message. Output: {result.stdout}"

    # Check if the script actually contains the required elements
    with open(script_path, "r") as f:
        script_content = f.read()

    assert "req-test-999" in script_content, "Regression test script does not contain the synthetic req_id 'req-test-999'."
    assert "/home/user/ingestion_system/process.sh" in script_content, "Regression test script does not call the process.sh script."