# test_final_state.py

import os
import json
import pytest

REPORT_PATH = '/home/user/monitor/report.txt'
ENDPOINTS_PATH = '/home/user/monitor/endpoints.json'

def test_endpoints_json_is_valid():
    assert os.path.isfile(ENDPOINTS_PATH), f"{ENDPOINTS_PATH} is missing."
    try:
        with open(ENDPOINTS_PATH, 'r') as f:
            data = json.load(f)
        assert "sites" in data, "endpoints.json must contain a 'sites' key."
        assert isinstance(data["sites"], list), "'sites' in endpoints.json must be a list."
    except json.JSONDecodeError as e:
        pytest.fail(f"endpoints.json is not valid JSON. Did you remove the trailing comma? Error: {e}")

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The report file {REPORT_PATH} was not generated. Did you run the script?"

def test_report_content():
    assert os.path.isfile(REPORT_PATH), f"The report file {REPORT_PATH} is missing."

    expected_lines = [
        "http://localhost:8080/good1 - UP",
        "http://localhost:8080/good2 - UP",
        "http://localhost:8080/bad - DOWN"
    ]

    with open(REPORT_PATH, 'r') as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report, but found {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual}'"