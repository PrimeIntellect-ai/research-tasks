# test_final_state.py

import os
import stat
import subprocess
import socket
import time
import pytest

BASE_DIR = "/home/user/ci-runner"

def test_files_exist():
    """Verify that all required files and directories exist."""
    required_files = [
        "roles.conf",
        "main.go",
        "pipeline.sh",
        "bin/runner",
        "test.log"
    ]
    for filename in required_files:
        path = os.path.join(BASE_DIR, filename)
        assert os.path.exists(path), f"Required file {path} does not exist."

def test_roles_conf_content():
    """Verify the content of roles.conf."""
    roles_path = os.path.join(BASE_DIR, "roles.conf")
    with open(roles_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "alice:dev:deploy,status",
        "bob:admin:deploy,status,restart",
        "charlie:qa:status"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert actual_lines == expected_lines, "roles.conf does not contain the exact expected mappings."

def test_pipeline_sh_executable():
    """Verify that pipeline.sh is executable."""
    pipeline_path = os.path.join(BASE_DIR, "pipeline.sh")
    st = os.stat(pipeline_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{pipeline_path} is not executable."

def test_test_log_content():
    """Verify the content of test.log."""
    log_path = os.path.join(BASE_DIR, "test.log")
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "ACCESS_GRANTED", f"test.log content is '{content}', expected 'ACCESS_GRANTED'."

def get_free_port():
    """Helper to get an available port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def test_runner_binary_behavior():
    """Verify the behavior of the compiled Go binary."""
    runner_path = os.path.join(BASE_DIR, "bin/runner")

    port = get_free_port()

    # Start a dummy listener
    listener = subprocess.Popen(["nc", "-l", str(port)])
    time.sleep(0.5) # Give nc time to start listening

    try:
        # Test 1: charlie deploy (Unauthorized, but reachable)
        result1 = subprocess.run(
            [runner_path, "charlie", "deploy", f"localhost:{port}"],
            capture_output=True, text=True
        )
        assert result1.returncode == 3, f"Expected exit code 3 for unauthorized user, got {result1.returncode}"
        assert "ACCESS_DENIED" in result1.stdout, f"Expected 'ACCESS_DENIED' in stdout, got {result1.stdout}"

        # Test 2: alice deploy (Authorized, reachable)
        # We need to restart the listener because nc -l exits after one connection
        listener.terminate()
        listener.wait()

        listener = subprocess.Popen(["nc", "-l", str(port)])
        time.sleep(0.5)

        result2 = subprocess.run(
            [runner_path, "alice", "deploy", f"localhost:{port}"],
            capture_output=True, text=True
        )
        assert result2.returncode == 0, f"Expected exit code 0 for authorized user, got {result2.returncode}"
        assert "ACCESS_GRANTED" in result2.stdout, f"Expected 'ACCESS_GRANTED' in stdout, got {result2.stdout}"

    finally:
        listener.terminate()
        listener.wait()

    # Test 3: bob deploy (Authorized, but unreachable)
    bad_port = get_free_port() # No listener on this port
    result3 = subprocess.run(
        [runner_path, "bob", "deploy", f"localhost:{bad_port}"],
        capture_output=True, text=True
    )
    assert result3.returncode == 2, f"Expected exit code 2 for unreachable endpoint, got {result3.returncode}"
    assert "ENDPOINT_UNREACHABLE" in result3.stdout, f"Expected 'ENDPOINT_UNREACHABLE' in stdout, got {result3.stdout}"