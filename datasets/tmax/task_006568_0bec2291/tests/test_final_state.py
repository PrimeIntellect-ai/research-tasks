# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/observability_report.json"
STATE_DIR = "/home/user/mock_containers"

def test_report_exists_and_valid_json():
    assert os.path.exists(REPORT_PATH), f"Report file not found at {REPORT_PATH}."
    assert os.path.isfile(REPORT_PATH), f"Path {REPORT_PATH} is not a file."

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Report file {REPORT_PATH} is not valid JSON: {e}")

    assert "restarted_containers" in data, "Key 'restarted_containers' missing from JSON report."
    assert "ui_errors" in data, "Key 'ui_errors' missing from JSON report."

def test_restarted_containers_in_report():
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    restarted = data.get("restarted_containers", [])
    assert isinstance(restarted, list), "'restarted_containers' must be a list."

    expected_restarted = {"def20002", "jkl40004"}
    actual_restarted = set(restarted)

    assert actual_restarted == expected_restarted, (
        f"Expected restarted_containers to be {expected_restarted}, "
        f"but got {actual_restarted}."
    )

def test_ui_errors_in_report():
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    ui_errors = data.get("ui_errors", {})
    assert isinstance(ui_errors, dict), "'ui_errors' must be a dictionary."

    expected_errors = {
        "abc10001": ["Widget 'Network' timeout."],
        "def20002": ["Out of memory in panel 'Disk'."],
        "jkl40004": ["Widget 'CPU' timeout.", "Alert manager disconnected."]
    }

    assert set(ui_errors.keys()) == set(expected_errors.keys()), (
        f"Expected ui_errors keys {set(expected_errors.keys())}, "
        f"but got {set(ui_errors.keys())}."
    )

    for container_id, expected_msgs in expected_errors.items():
        actual_msgs = ui_errors[container_id]
        assert isinstance(actual_msgs, list), f"Errors for {container_id} must be a list."
        assert actual_msgs == expected_msgs, (
            f"Expected errors for {container_id} to be {expected_msgs}, "
            f"but got {actual_msgs}."
        )

def test_containers_were_actually_restarted():
    # Check that high-memory containers were actually restarted via the script
    c2_mem_path = os.path.join(STATE_DIR, "c2_mem")
    c4_mem_path = os.path.join(STATE_DIR, "c4_mem")

    assert os.path.exists(c2_mem_path), f"State file {c2_mem_path} missing."
    assert os.path.exists(c4_mem_path), f"State file {c4_mem_path} missing."

    with open(c2_mem_path, 'r') as f:
        c2_mem = f.read().strip()
    with open(c4_mem_path, 'r') as f:
        c4_mem = f.read().strip()

    assert c2_mem == "100MB", f"Container def20002 was not restarted. Expected memory '100MB', got '{c2_mem}'."
    assert c4_mem == "100MB", f"Container jkl40004 was not restarted. Expected memory '100MB', got '{c4_mem}'."

def test_containers_were_not_incorrectly_restarted():
    # Check that normal-memory containers were NOT restarted
    c1_mem_path = os.path.join(STATE_DIR, "c1_mem")
    c3_mem_path = os.path.join(STATE_DIR, "c3_mem")

    assert os.path.exists(c1_mem_path), f"State file {c1_mem_path} missing."
    assert os.path.exists(c3_mem_path), f"State file {c3_mem_path} missing."

    with open(c1_mem_path, 'r') as f:
        c1_mem = f.read().strip()
    with open(c3_mem_path, 'r') as f:
        c3_mem = f.read().strip()

    assert c1_mem == "250MB", f"Container abc10001 should not have been restarted. Expected memory '250MB', got '{c1_mem}'."
    assert c3_mem == "150MB", f"Container ghi30003 should not have been restarted. Expected memory '150MB', got '{c3_mem}'."