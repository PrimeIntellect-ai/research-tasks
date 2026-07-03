# test_final_state.py

import os
import json
import re
import pytest

def test_anomalies_json_exists_and_correct():
    json_path = "/home/user/anomalies.json"
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            anomalies = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected_anomalies = [
        "machine_03.csv",
        "machine_07.csv",
        "machine_08.csv",
        "machine_14.csv",
        "machine_19.csv"
    ]

    assert isinstance(anomalies, list), f"Expected a JSON list in {json_path}."
    assert anomalies == expected_anomalies, f"Anomalies list incorrect. Expected {expected_anomalies}, got {anomalies}."

def test_pipeline_log_exists_and_format():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) >= 20, f"Log file should have at least 20 lines, found {len(lines)}."

    # Check if there are 20 lines matching the required pattern
    # Pattern: %(asctime)s - %(levelname)s - Processed %(filename)s - Distance: %(distance).2f - Changepoint: %(changepoint)s
    # Example: 2023-10-25 12:34:56,789 - INFO - Processed machine_01.csv - Distance: 15.23 - Changepoint: False
    pattern = re.compile(r".* - INFO - Processed machine_\d{2}\.csv - Distance: \d+\.\d{2} - Changepoint: (True|False)")

    matched_lines = [line for line in lines if pattern.match(line)]
    assert len(matched_lines) == 20, f"Expected exactly 20 log lines matching the required format, found {len(matched_lines)}."

    # Check that all 20 machines are logged
    machines_logged = set()
    for line in matched_lines:
        match = re.search(r"Processed (machine_\d{2}\.csv)", line)
        if match:
            machines_logged.add(match.group(1))

    assert len(machines_logged) == 20, "Not all 20 machines were logged."