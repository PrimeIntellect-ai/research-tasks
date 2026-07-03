# test_final_state.py

import os
import json
import pytest

def test_c_file_exists():
    """Test that the C source file was created."""
    c_file_path = "/home/user/workspace/detect_deadlock.c"
    assert os.path.isfile(c_file_path), f"C source file is missing at {c_file_path}"

def test_json_report_exists():
    """Test that the deadlock report JSON file was created."""
    json_path = "/home/user/workspace/deadlock_report.json"
    assert os.path.isfile(json_path), f"JSON report is missing at {json_path}"

def test_json_report_content():
    """Test that the deadlock report contains the correct cycle."""
    json_path = "/home/user/workspace/deadlock_report.json"

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "cycle" in data, "JSON report is missing the 'cycle' key."

    cycle = data["cycle"]
    assert isinstance(cycle, list), "The 'cycle' value must be a list."

    expected_cycle = [101, 102, 103]
    assert cycle == expected_cycle, f"Expected cycle {expected_cycle}, but got {cycle}."