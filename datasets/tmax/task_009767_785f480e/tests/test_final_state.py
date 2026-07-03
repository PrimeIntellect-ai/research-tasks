# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_deployed_executable_exists():
    """Check that the deployed auth_daemon exists and is executable."""
    executable_path = "/home/user/deploy/bin/auth_daemon"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_deploy_log_contents():
    """Check that the deploy log exists and contains the correct string."""
    log_path = "/home/user/deploy/deploy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "CI pipeline passed", f"Log file content is incorrect. Expected 'CI pipeline passed', got '{content}'."

def test_bashrc_path_modification():
    """Check that .bashrc contains the correct PATH modification."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."
    expected_line = "export PATH=$PATH:/home/user/deploy/bin"

    with open(bashrc_path, "r") as f:
        lines = f.read().splitlines()

    assert expected_line in lines, f"{bashrc_path} does not contain the expected PATH export line."

def test_auth_daemon_functionality():
    """Test the compiled C program dynamically to ensure it behaves correctly."""
    executable_path = "/home/user/deploy/bin/auth_daemon"
    assert os.path.isfile(executable_path), "Cannot test auth_daemon: file not found."

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_store:
        temp_store.write("testuser1\nadmin\n")
        temp_store_path = temp_store.name

    try:
        env = os.environ.copy()
        env["AUTH_STORE"] = temp_store_path

        # Test case 1: Valid user, Invalid user, QUIT
        input_data = "testuser1\nbaduser\nQUIT\n"
        process = subprocess.run(
            [executable_path],
            input=input_data,
            text=True,
            env=env,
            capture_output=True
        )

        assert process.returncode == 0, f"auth_daemon exited with non-zero status {process.returncode} when QUIT was sent."

        output = process.stdout
        assert "Access Granted" in output, "Expected 'Access Granted' in output for valid user."
        assert "Access Denied" in output, "Expected 'Access Denied' in output for invalid user."

        # Test case 2: No AUTH_STORE
        env_no_store = os.environ.copy()
        if "AUTH_STORE" in env_no_store:
            del env_no_store["AUTH_STORE"]

        process_no_store = subprocess.run(
            [executable_path],
            input="QUIT\n",
            text=True,
            env=env_no_store,
            capture_output=True
        )
        assert process_no_store.returncode == 1, "auth_daemon should exit with status 1 if AUTH_STORE is not set."

    finally:
        if os.path.exists(temp_store_path):
            os.remove(temp_store_path)