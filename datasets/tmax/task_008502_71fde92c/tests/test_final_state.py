# test_final_state.py
import os
import json
import re
import pytest

SCRIPT_PATH = "/home/user/process_logs.sh"
OUTPUT_PATH = "/home/user/stratified_sample.jsonl"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_output_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

def test_output_format_and_content():
    if not os.path.isfile(OUTPUT_PATH):
        pytest.fail(f"Output file {OUTPUT_PATH} does not exist.")

    with open(OUTPUT_PATH, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"Output file {OUTPUT_PATH} is empty."

    status_counts = {}

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {OUTPUT_PATH} is not valid JSON: {line.strip()}")

        # Check keys
        expected_keys = {"timestamp", "ip_address", "status", "user_agent"}
        assert set(data.keys()) == expected_keys, f"Line {i+1} does not have exactly the required keys. Found: {list(data.keys())}"

        # Count statuses
        status = data["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

        # Check IP masking
        ip = data["ip_address"]
        assert re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.0$", ip), f"IP address {ip} on line {i+1} is not masked properly (should end in .0)."

        # Check timestamp
        ts = data["timestamp"]
        assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", ts), f"Timestamp {ts} on line {i+1} is not in strict ISO 8601 UTC format."

        # Check user_agent for malformed unicode
        ua = data["user_agent"]
        assert r"\u" not in ua, f"Malformed unicode might still be present in user_agent on line {i+1}: {ua}"

    # Original data has statuses 200, 404, 500
    expected_statuses = {200, 404, 500}
    assert set(status_counts.keys()) == expected_statuses, f"Expected statuses {expected_statuses}, but found {set(status_counts.keys())}"

    for status, count in status_counts.items():
        assert count == 3, f"Expected exactly 3 samples for status {status}, but found {count}."