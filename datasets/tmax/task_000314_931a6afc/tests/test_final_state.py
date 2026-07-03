# test_final_state.py

import os
import json
import pytest

def test_env_file_updated():
    env_path = "/home/user/app/.env"
    assert os.path.isfile(env_path), f"File {env_path} is missing"

    with open(env_path, "r") as f:
        content = f.read()

    assert "API_TIMEOUT_MS" in content, "The .env file must contain the corrected key 'API_TIMEOUT_MS'"
    assert "API_TIMEOUT_S" not in content, "The .env file should no longer contain the incorrect key 'API_TIMEOUT_S'"

def test_diagnostic_report_exists_and_valid():
    report_path = "/home/user/diagnostic_report.json"
    assert os.path.isfile(report_path), f"Diagnostic report {report_path} was not generated"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON")

    assert "misconfigured_key" in data, "JSON missing 'misconfigured_key'"
    assert "corrected_value" in data, "JSON missing 'corrected_value'"
    assert "timeline" in data, "JSON missing 'timeline'"

def test_diagnostic_report_contents():
    report_path = "/home/user/diagnostic_report.json"
    if not os.path.isfile(report_path):
        pytest.skip("Report not found")

    with open(report_path, "r") as f:
        data = json.load(f)

    assert data["misconfigured_key"] == "API_TIMEOUT_S", "misconfigured_key should be 'API_TIMEOUT_S'"

    # Verify the corrected value matches the .env file
    env_path = "/home/user/app/.env"
    env_val = None
    if os.path.isfile(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("API_TIMEOUT_MS="):
                    env_val = line.strip().split("=", 1)[1]

    if env_val:
        assert str(data["corrected_value"]) == env_val, "corrected_value in JSON does not match the value in .env"

def test_diagnostic_report_timeline():
    report_path = "/home/user/diagnostic_report.json"
    if not os.path.isfile(report_path):
        pytest.skip("Report not found")

    with open(report_path, "r") as f:
        data = json.load(f)

    timeline = data.get("timeline", [])
    assert len(timeline) == 6, f"Expected 6 events for REQ-008, found {len(timeline)}"

    expected_events = [
        {"service": "frontend", "timestamp": "2023-10-01T10:05:01.000Z", "message": "Received request from client"},
        {"service": "frontend", "timestamp": "2023-10-01T10:05:01.010Z", "message": "Forwarding to backend"},
        {"service": "backend", "timestamp": "2023-10-01T10:05:01.015Z", "message": "Backend received payload"},
        {"service": "backend", "timestamp": "2023-10-01T10:05:01.035Z", "message": "Database query started"},
        {"service": "frontend", "timestamp": "2023-10-01T10:05:01.040Z", "message": "Timeout exceeded while waiting for backend"},
        {"service": "backend", "timestamp": "2023-10-01T10:05:01.200Z", "message": "Database query finished"}
    ]

    # Check that events are sorted chronologically and match expected
    for i, (actual, expected) in enumerate(zip(timeline, expected_events)):
        assert actual.get("service") == expected["service"], f"Event {i} service mismatch"
        assert actual.get("timestamp") == expected["timestamp"], f"Event {i} timestamp mismatch (possibly not sorted chronologically)"
        assert actual.get("message") == expected["message"], f"Event {i} message mismatch"