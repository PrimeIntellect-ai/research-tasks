# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_api_running_and_correct():
    url = "http://127.0.0.1:8080/verify"
    headers = {"Authorization": "Bearer delta charlie seven"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Service B at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response body: {response.text}"

def test_acls_configured():
    config_dir = "/home/user/config"
    assert os.path.exists(config_dir), f"Directory {config_dir} does not exist."

    result = subprocess.run(["getfacl", config_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run getfacl on {config_dir}"

    # Check if nobody has read access in the ACL
    acl_output = result.stdout
    assert "user:nobody:r" in acl_output, f"ACLs for user 'nobody' not configured correctly on {config_dir}. getfacl output:\n{acl_output}"

def test_migration_log_exists():
    log_path = "/home/user/migration.log"
    assert os.path.exists(log_path), f"Migration log {log_path} is missing."
    with open(log_path, 'r') as f:
        content = f.read()

    assert "Service A" in content, f"Migration log missing Service A status. Content:\n{content}"
    assert "Service B" in content, f"Migration log missing Service B status. Content:\n{content}"

def test_passcode_file_exists():
    passcode_path = "/home/user/config/passcode.txt"
    assert os.path.exists(passcode_path), f"Passcode file {passcode_path} is missing."
    with open(passcode_path, 'r') as f:
        content = f.read().strip()
    assert content == "delta charlie seven", f"Passcode file contains '{content}', expected 'delta charlie seven'"