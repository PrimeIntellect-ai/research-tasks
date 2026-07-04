# test_final_state.py

import os
import json
import subprocess
import pytest

def test_investigate_script_exists_and_executable():
    script_path = "/home/user/investigate.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_script_execution_and_report_generation():
    script_path = "/home/user/investigate.sh"
    report_path = "/home/user/summary_report.json"

    # Remove the report if it exists from a previous run
    if os.path.exists(report_path):
        os.remove(report_path)

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.isfile(report_path), f"The report file {report_path} was not created by the script."

def test_summary_report_contents():
    report_path = "/home/user/summary_report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {report_path} as JSON: {e}")

    assert "cracked_password" in report_data, "Missing 'cracked_password' key in JSON report."
    assert report_data["cracked_password"] == "supernova_admin", "The cracked password does not match the expected value."

    assert "certificate_valid" in report_data, "Missing 'certificate_valid' key in JSON report."
    assert isinstance(report_data["certificate_valid"], bool), "The 'certificate_valid' value must be a boolean."
    assert report_data["certificate_valid"] is True, "The certificate should be valid."

    assert "script_src_values" in report_data, "Missing 'script_src_values' key in JSON report."
    expected_script_src = ["'self'", "https://scripts.trusted.com", "https://cdn.malicious.local"]
    assert isinstance(report_data["script_src_values"], list), "The 'script_src_values' must be a list."
    assert report_data["script_src_values"] == expected_script_src, f"The script_src_values do not match the expected list. Got: {report_data['script_src_values']}"