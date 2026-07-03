# test_final_state.py
import os
import json
import stat
import pytest

def test_monitor_go_exists():
    assert os.path.isfile("/home/user/monitor.go"), "/home/user/monitor.go is missing"

def test_run_monitor_sh_exists_and_executable():
    script_path = "/home/user/run_monitor.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

def test_monitor_bin_exists():
    bin_path = "/home/user/monitor_bin"
    assert os.path.isfile(bin_path), f"{bin_path} is missing. Did the script compile the Go program?"

def test_alerts_json_content():
    json_path = "/home/user/alerts.json"
    assert os.path.isfile(json_path), f"{json_path} is missing. Did the program run successfully?"

    with open(json_path, "r") as f:
        try:
            alerts = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON")

    expected_alerts = [
        {"timestamp": "2023-10-25T21:30:00Z", "service": "auth-service", "group": "sec-ops"},
        {"timestamp": "2023-10-26T00:00:00Z", "service": "payment-service", "group": "fin-ops"},
        {"timestamp": "2023-10-26T01:20:00Z", "service": "unknown-service", "group": "unknown"}
    ]

    assert isinstance(alerts, list), f"Expected alerts to be a JSON array, got {type(alerts).__name__}"
    assert len(alerts) == len(expected_alerts), f"Expected {len(expected_alerts)} alerts, but found {len(alerts)}"

    for i, (actual, expected) in enumerate(zip(alerts, expected_alerts)):
        assert actual == expected, f"Alert at index {i} does not match expected output.\nExpected: {expected}\nActual: {actual}"