# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/investigation/report.json"

def test_report_exists():
    """Test that the final report.json file has been created."""
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist. Did you save your output?"

def test_report_is_valid_json():
    """Test that the report.json file contains valid JSON."""
    with open(REPORT_PATH, "r") as f:
        try:
            json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON: {e}")

def test_report_content_and_structure():
    """Test that the report contains the correct redacted IPs and endpoints for valid JWTs."""
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert isinstance(data, list), f"Expected the root of the JSON to be an array, but got {type(data).__name__}."
    assert len(data) == 2, f"Expected exactly 2 valid JWT entries in the report, but found {len(data)}."

    # Validate first entry
    entry1 = data[0]
    assert "timestamp" in entry1, "First entry is missing the 'timestamp' key."
    assert entry1.get("endpoint") == "/api/v1/admin/dump", f"First entry endpoint is incorrect. Got: {entry1.get('endpoint')}"
    assert entry1.get("redacted_ip") == "10.4.5.XXX", f"First entry redacted_ip is incorrect. Got: {entry1.get('redacted_ip')}"

    # Validate second entry
    entry2 = data[1]
    assert "timestamp" in entry2, "Second entry is missing the 'timestamp' key."
    assert entry2.get("endpoint") == "/api/v1/system/keys", f"Second entry endpoint is incorrect. Got: {entry2.get('endpoint')}"
    assert entry2.get("redacted_ip") == "8.8.8.XXX", f"Second entry redacted_ip is incorrect. Got: {entry2.get('redacted_ip')}"