# test_final_state.py

import os
import json
import pytest

def test_process_script_exists():
    script_path = "/home/user/process.sh"
    assert os.path.exists(script_path), f"The script file {script_path} does not exist. You must create it."
    assert os.path.isfile(script_path), f"{script_path} is not a regular file."

def test_alerts_jsonl_exists_and_content():
    alerts_path = "/home/user/alerts.jsonl"
    assert os.path.exists(alerts_path), f"The output file {alerts_path} does not exist."
    assert os.path.isfile(alerts_path), f"{alerts_path} is not a regular file."

    expected_data = [
        {"alert_type": "HighTemp", "timestamp": "2023-10-12T08:02:00Z", "sensor": "S-303", "reading": 91.5},
        {"alert_type": "HighTemp", "timestamp": "2023-10-12T08:04:00Z", "sensor": "S-505", "reading": 90.1},
        {"alert_type": "HighTemp", "timestamp": "2023-10-12T08:07:00Z", "sensor": "S-808", "reading": 105.3}
    ]

    actual_data = []
    with open(alerts_path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
                actual_data.append(parsed)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {alerts_path} is not valid JSON: {line}")

    assert len(actual_data) == len(expected_data), (
        f"Expected {len(expected_data)} alerts, but found {len(actual_data)} in {alerts_path}."
    )

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, (
            f"Alert at line {i+1} does not match expected output.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )