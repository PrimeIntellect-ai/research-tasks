# test_final_state.py

import os
import json
import stat
import subprocess
import time
import socket
import pytest

DIAG_DIR = "/home/user/network_diag"
SETUP_SCRIPT = os.path.join(DIAG_DIR, "setup.sh")
ROLES_JSON = os.path.join(DIAG_DIR, "roles.json")
DIAG_TOOL = os.path.join(DIAG_DIR, "diag_tool")
AUDIT_LOG = os.path.join(DIAG_DIR, "audit.log")

def test_setup_script_exists_and_executable():
    assert os.path.isfile(SETUP_SCRIPT), f"{SETUP_SCRIPT} does not exist."
    st = os.stat(SETUP_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{SETUP_SCRIPT} is not executable."

def test_roles_json_content():
    assert os.path.isfile(ROLES_JSON), f"{ROLES_JSON} does not exist."
    with open(ROLES_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{ROLES_JSON} is not valid JSON.")

    expected = {
        "netadmin": ["127.0.0.1:9001", "127.0.0.1:9002", "127.0.0.1:9003"],
        "appdev": ["127.0.0.1:9001"],
        "guest": ["127.0.0.1:9003"]
    }
    assert data == expected, f"Contents of {ROLES_JSON} do not match the expected configuration."

def test_diag_tool_exists_and_executable():
    assert os.path.isfile(DIAG_TOOL), f"{DIAG_TOOL} does not exist. Did setup.sh compile it?"
    st = os.stat(DIAG_TOOL)
    assert bool(st.st_mode & stat.S_IXUSR), f"{DIAG_TOOL} is not executable."

def wait_for_port(port, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return True
        time.sleep(0.1)
    return False

def test_diag_tool_invalid_user():
    # Run the tool with an invalid user
    process = subprocess.Popen(
        [DIAG_TOOL],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input="hacker\n", timeout=2)

    assert process.returncode == 1, f"Expected exit code 1 for invalid user, got {process.returncode}."
    assert "Access Denied" in stdout or "Access Denied" in stderr, "Expected 'Access Denied' output for invalid user."

def test_diag_tool_valid_user_and_audit_log():
    # Start listeners on 9001 and 9002
    p1 = subprocess.Popen(["python3", "-m", "http.server", "9001"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p2 = subprocess.Popen(["python3", "-m", "http.server", "9002"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        assert wait_for_port(9001), "Failed to start listener on port 9001 for testing."
        assert wait_for_port(9002), "Failed to start listener on port 9002 for testing."

        # Ensure port 9003 is closed
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            assert s.connect_ex(('127.0.0.1', 9003)) != 0, "Port 9003 should be closed for this test."

        # Clear audit log if it exists
        if os.path.exists(AUDIT_LOG):
            os.remove(AUDIT_LOG)

        # Run the tool with valid user 'netadmin'
        process = subprocess.Popen(
            [DIAG_TOOL],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input="netadmin\n", timeout=5)

        assert process.returncode == 0, f"Expected exit code 0 for valid user, got {process.returncode}."

        assert os.path.isfile(AUDIT_LOG), f"{AUDIT_LOG} was not created."

        with open(AUDIT_LOG, "r") as f:
            log_contents = f.read()

        expected_lines = [
            "[netadmin] checked 127.0.0.1:9001: OK",
            "[netadmin] checked 127.0.0.1:9002: OK",
            "[netadmin] checked 127.0.0.1:9003: FAIL"
        ]

        for line in expected_lines:
            assert line in log_contents, f"Expected line '{line}' not found in {AUDIT_LOG}. Log contents:\n{log_contents}"

    finally:
        p1.terminate()
        p2.terminate()
        p1.wait()
        p2.wait()