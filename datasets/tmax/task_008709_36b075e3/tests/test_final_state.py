# test_final_state.py

import os
import json
import subprocess
import pytest

def test_audit_script_exists_and_executable():
    script_path = "/home/user/audit.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_charlie_access_json():
    output_path = "/home/user/charlie_access.json"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_content = """[
  {"user": "u_charlie", "resource": "res_db_main"},
  {"user": "u_charlie", "resource": "res_server_1"}
]"""

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {output_path} does not match the strict expected JSON format."

def test_audit_script_functionality_bob():
    script_path = "/home/user/audit.sh"

    try:
        result = subprocess.run([script_path, "u_bob"], capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("Script timed out, possible infinite loop.")

    assert result.returncode == 0, "Script failed to execute successfully for u_bob."

    expected_content = """[
  {"user": "u_bob", "resource": "res_dashboard"}
]"""

    assert result.stdout.strip() == expected_content, "Script output for u_bob does not match the expected JSON format."

def test_audit_script_functionality_alice():
    script_path = "/home/user/audit.sh"

    try:
        result = subprocess.run([script_path, "u_alice"], capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("Script timed out, possible infinite loop.")

    assert result.returncode == 0, "Script failed to execute successfully for u_alice."

    expected_content = """[
  {"user": "u_alice", "resource": "res_db_main"},
  {"user": "u_alice", "resource": "res_server_1"}
]"""

    assert result.stdout.strip() == expected_content, "Script output for u_alice does not match the expected JSON format."