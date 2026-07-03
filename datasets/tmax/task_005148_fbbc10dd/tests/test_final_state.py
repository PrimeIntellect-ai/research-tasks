# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_file_exists():
    """Test that the report.json file was generated."""
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} is missing."

def test_report_is_valid_json():
    """Test that the report.json file contains valid JSON."""
    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Report file {REPORT_PATH} is not valid JSON: {e}")
    assert isinstance(data, dict), "The root of the JSON report must be an object (dictionary)."

def test_report_contents():
    """Test that the report.json contains the expected analysis of the backup files."""
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    # 1. invalid.bak should be missing
    assert "invalid.bak" not in data, "invalid.bak should not be included in the report because of invalid magic bytes."

    # 2. Expected files should be present
    expected_files = ["safe1.bak", "malicious_abs.bak", "malicious_rel.bak"]
    for filename in expected_files:
        assert filename in data, f"{filename} is missing from the JSON report."

    # 3. Check safe1.bak
    safe1 = data["safe1.bak"]
    assert safe1.get("total_entries") == 2, f"safe1.bak total_entries should be 2, got {safe1.get('total_entries')}"
    assert isinstance(safe1.get("dangerous_paths"), list), "safe1.bak dangerous_paths must be a list"
    assert len(safe1["dangerous_paths"]) == 0, f"safe1.bak should have no dangerous paths, got {safe1['dangerous_paths']}"

    # 4. Check malicious_abs.bak
    mal_abs = data["malicious_abs.bak"]
    assert mal_abs.get("total_entries") == 3, f"malicious_abs.bak total_entries should be 3, got {mal_abs.get('total_entries')}"
    expected_abs_paths = {"/etc/shadow", "/root/.ssh/authorized_keys"}
    actual_abs_paths = set(mal_abs.get("dangerous_paths", []))
    assert actual_abs_paths == expected_abs_paths, f"malicious_abs.bak dangerous paths mismatch. Expected {expected_abs_paths}, got {actual_abs_paths}"

    # 5. Check malicious_rel.bak
    mal_rel = data["malicious_rel.bak"]
    assert mal_rel.get("total_entries") == 3, f"malicious_rel.bak total_entries should be 3, got {mal_rel.get('total_entries')}"
    expected_rel_paths = {"../../.bashrc", "folder/../../usr/bin/python"}
    actual_rel_paths = set(mal_rel.get("dangerous_paths", []))
    assert actual_rel_paths == expected_rel_paths, f"malicious_rel.bak dangerous paths mismatch. Expected {expected_rel_paths}, got {actual_rel_paths}"