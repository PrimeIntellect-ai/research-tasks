# test_final_state.py

import os
import json
import pytest

def test_analyze_script_exists():
    path = "/home/user/analyze.py"
    assert os.path.isfile(path), f"The script {path} does not exist."

def test_report_exists():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"The report file {path} does not exist. Ensure your script creates it."

def test_report_content():
    path = "/home/user/report.json"

    if not os.path.isfile(path):
        pytest.fail(f"Cannot test content because {path} is missing.")

    try:
        with open(path, "r") as f:
            report_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {path} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {path}: {e}")

    # Expected values based on the setup
    expected_cwe = "CWE-78"
    expected_ip = "172.16.22.109"
    expected_file = "persistence_bind.sh"

    # Validate CWE
    assert "cwe" in report_data, "The JSON report is missing the 'cwe' key."
    assert report_data["cwe"] == expected_cwe, f"Incorrect CWE. Expected '{expected_cwe}', got '{report_data['cwe']}'."

    # Validate Attacker IP
    assert "attacker_ip" in report_data, "The JSON report is missing the 'attacker_ip' key."
    assert report_data["attacker_ip"] == expected_ip, f"Incorrect attacker IP. Expected '{expected_ip}', got '{report_data['attacker_ip']}'."

    # Validate World Writable File
    assert "world_writable_file" in report_data, "The JSON report is missing the 'world_writable_file' key."
    assert report_data["world_writable_file"] == expected_file, f"Incorrect world writable file. Expected '{expected_file}', got '{report_data['world_writable_file']}'."