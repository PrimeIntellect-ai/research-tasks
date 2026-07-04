# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_exploit_script_exists_and_executable():
    exploit_path = "/home/user/exploit.sh"
    assert os.path.exists(exploit_path), f"Missing exploit script: {exploit_path}"
    assert os.path.isfile(exploit_path), f"Not a file: {exploit_path}"
    assert os.access(exploit_path, os.X_OK), f"Exploit script is not executable: {exploit_path}"

def test_exploit_execution_and_result():
    exploit_path = "/home/user/exploit.sh"
    flag_path = "/home/user/hidden_flag.txt"
    success_path = "/home/user/success.txt"

    # Ensure the success.txt doesn't already exist or remove it to ensure the script creates it
    if os.path.exists(success_path):
        os.remove(success_path)

    # Run the exploit script
    result = subprocess.run([exploit_path], capture_output=True, text=True, cwd="/home/user")

    assert result.returncode == 0 or os.path.exists(success_path), (
        f"Execution of {exploit_path} failed or did not create {success_path}. "
        f"Stdout: {result.stdout}, Stderr: {result.stderr}"
    )

    assert os.path.exists(success_path), f"The file {success_path} was not created by the exploit script."

    # Read the original flag
    with open(flag_path, "r") as f:
        expected_flag = f.read().strip()

    # Read the success output
    with open(success_path, "r") as f:
        actual_flag = f.read().strip()

    assert actual_flag == expected_flag, (
        f"The content of {success_path} does not match {flag_path}. "
        f"Expected: {expected_flag}, Got: {actual_flag}"
    )