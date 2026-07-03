# test_final_state.py
import os
import json
import pytest

def test_uptime_report_exists():
    path = "/home/user/uptime_report.json"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the fixed Go program?"

def test_uptime_report_content():
    path = "/home/user/uptime_report.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert "longest_downtime_minutes" in data, "Key 'longest_downtime_minutes' missing from JSON."
    assert "uptime_percentage" in data, "Key 'uptime_percentage' missing from JSON."

    assert data["longest_downtime_minutes"] == 15, f"Expected longest_downtime_minutes to be 15, got {data['longest_downtime_minutes']}"

    # Check uptime percentage with some tolerance or exact match
    expected_pct = 85.15
    actual_pct = data["uptime_percentage"]
    assert abs(actual_pct - expected_pct) < 0.01, f"Expected uptime_percentage to be 85.15, got {actual_pct}"

def test_main_go_bugs_fixed():
    path = "/home/user/uptime_calculator/main.go"
    if not os.path.isfile(path):
        pytest.skip("main.go not found, skipping source check.")

    with open(path, 'r') as f:
        content = f.read()

    assert "i <= len(pings)" not in content, "Bug 1 (off-by-one boundary error) is still present in main.go"
    assert "p.Timestamp < endTS" not in content, "Bug 2 (exclusive boundary condition) is still present in main.go"