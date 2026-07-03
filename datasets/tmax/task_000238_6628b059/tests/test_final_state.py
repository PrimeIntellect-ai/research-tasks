# test_final_state.py

import os
import json
import pytest

SCRIPT_PATH = "/home/user/audit_pipeline.py"
OUTPUT_PATH = "/home/user/suspicious_users.json"

def test_audit_pipeline_script_exists():
    """Test that the Python script was created."""
    assert os.path.exists(SCRIPT_PATH), f"Python script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_suspicious_users_json_exists():
    """Test that the output JSON file was created."""
    assert os.path.exists(OUTPUT_PATH), f"Output JSON file missing at {OUTPUT_PATH}"
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} is not a file"

def test_suspicious_users_json_content():
    """Test that the output JSON file contains the correct flagged users."""
    assert os.path.exists(OUTPUT_PATH), f"Output JSON file missing at {OUTPUT_PATH}"

    with open(OUTPUT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} is not valid JSON")

    assert "flagged_users" in data, "JSON missing 'flagged_users' key"

    flagged_users = data["flagged_users"]
    assert isinstance(flagged_users, list), "'flagged_users' must be a list"

    expected_users = ["user_B", "user_C", "user_D"]
    assert flagged_users == expected_users, f"Expected flagged users {expected_users}, but got {flagged_users}"