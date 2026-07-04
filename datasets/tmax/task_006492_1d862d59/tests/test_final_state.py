# test_final_state.py

import os
import stat
import hashlib
import subprocess
import pytest

def test_recovered_token():
    secret_path = "/home/user/evidence/.secret_key"
    token_path = "/home/user/recovered_token.txt"

    assert os.path.isfile(secret_path), f"Secret key file {secret_path} is missing."
    with open(secret_path, "r") as f:
        secret = f.read().strip()

    expected_string = f"forensic_admin:1715000000:{secret}"
    expected_token = hashlib.sha256(expected_string.encode('utf-8')).hexdigest()

    assert os.path.isfile(token_path), f"Recovered token file {token_path} is missing."
    with open(token_path, "r") as f:
        actual_token = f.read().strip()

    assert actual_token == expected_token, f"The token in {token_path} is incorrect. Expected {expected_token}, got {actual_token}."

def test_exploited_binary():
    binary_path = "/home/user/exploited_binary.txt"
    assert os.path.isfile(binary_path), f"Exploited binary file {binary_path} is missing."

    with open(binary_path, "r") as f:
        actual_binary = f.read().strip()

    expected_binary = "/opt/internal/sys_backup_mgr"
    assert actual_binary == expected_binary, f"The exploited binary in {binary_path} is incorrect. Expected {expected_binary}, got {actual_binary}."

def test_auth_flow_script():
    script_path = "/home/user/test_auth_flow.sh"

    assert os.path.isfile(script_path), f"Auth flow script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    # Test script execution
    test_user = "testuser_123"
    test_timestamp = "9876543210"

    result = subprocess.run(
        [script_path, test_user, test_timestamp],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script {script_path} failed with exit code {result.returncode}. Output: {result.stdout}\nError: {result.stderr}"
    assert "AUTH SUCCESS" in result.stdout, f"Script {script_path} did not produce 'AUTH SUCCESS'. Output: {result.stdout}"