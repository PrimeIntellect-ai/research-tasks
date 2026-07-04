# test_final_state.py

import os
import subprocess
import pytest

def test_payload_execution():
    payload_path = "/home/user/payload.token"
    auth_gw_path = "/home/user/auth_gw"
    flag_path = "/home/user/flag.txt"
    result_path = "/home/user/result.log"

    assert os.path.exists(payload_path), f"Payload file {payload_path} does not exist."
    assert os.path.exists(auth_gw_path), f"Executable {auth_gw_path} does not exist."
    assert os.path.exists(flag_path), f"Flag file {flag_path} does not exist."

    # Read the expected flag
    with open(flag_path, "r") as f:
        expected_flag = f.read().strip()

    # Remove result.log if it exists to ensure the payload actually creates it
    if os.path.exists(result_path):
        os.remove(result_path)

    # Execute the payload
    try:
        result = subprocess.run([auth_gw_path, payload_path], capture_output=True, text=True)
    except Exception as e:
        pytest.fail(f"Failed to execute {auth_gw_path}: {e}")

    assert result.returncode == 0, f"Execution of auth_gw failed with return code {result.returncode}. stdout: {result.stdout.strip()}, stderr: {result.stderr.strip()}"

    assert os.path.exists(result_path), f"The file {result_path} was not created after executing the payload. Ensure your payload bypasses the filters and writes to {result_path}."

    # Read the actual result
    with open(result_path, "r") as f:
        actual_result = f.read().strip()

    assert actual_result == expected_flag, f"The content of {result_path} does not match the flag. Expected '{expected_flag}', got '{actual_result}'."