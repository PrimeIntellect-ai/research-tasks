# test_final_state.py

import os
import pytest

def test_triage_script_exists_and_executable():
    script_path = "/home/user/triage.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_incident_resolution_log():
    log_path = "/home/user/incident_resolution.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "SYSTEM_OK: FLAG{1nc1d3nt_r3s0lv3d}"
    assert expected_content in content, f"The log file does not contain the expected success message. Found: {content}"