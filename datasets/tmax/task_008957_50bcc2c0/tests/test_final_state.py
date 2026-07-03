# test_final_state.py

import os
import json
import pytest

def test_analyze_script_exists():
    """Verify that the analyze.py script was created."""
    path = "/home/user/analyze.py"
    assert os.path.isfile(path), f"The script {path} does not exist."

def test_report_json_exists():
    """Verify that the report.json file was generated."""
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"The report file {path} does not exist."

def test_report_json_content():
    """Verify the contents of the report.json file match the expected schema and values."""
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"The report file {path} does not exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {path} does not contain valid JSON.")

    expected_keys = {"subject_cn", "is_valid_ca", "privesc_command"}
    assert set(data.keys()) == expected_keys, f"The JSON schema is incorrect. Expected keys: {expected_keys}, found: {set(data.keys())}"

    assert data["subject_cn"] == "EvilCorp", f"Incorrect subject_cn. Expected 'EvilCorp', got '{data['subject_cn']}'"
    assert data["is_valid_ca"] is False, f"Incorrect is_valid_ca. Expected False, got {data['is_valid_ca']}"
    assert data["privesc_command"] == "sudo chmod u+s /bin/bash", f"Incorrect privesc_command. Expected 'sudo chmod u+s /bin/bash', got '{data['privesc_command']}'"