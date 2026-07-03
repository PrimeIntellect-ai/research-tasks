# test_final_state.py

import os
import subprocess
import time
import tempfile
import urllib.request
import pytest

DEPLOY_GIT = "/home/user/deploy.git"
LIVE_DIR = "/home/user/live"
HOOK_PATH = "/home/user/deploy.git/hooks/post-receive"
SOCAT_PID_FILE = "/home/user/socat.pid"
SERVER_LOG = "/home/user/server.log"

def test_bare_repo_exists():
    """Verify that the deploy.git directory is a bare git repository."""
    assert os.path.isdir(DEPLOY_GIT), f"{DEPLOY_GIT} directory does not exist."
    config_path = os.path.join(DEPLOY_GIT, "config")
    assert os.path.isfile(config_path), f"Git config not found at {config_path}."
    with open(config_path, "r") as f:
        content = f.read()
    assert "bare = true" in content.lower(), f"{DEPLOY_GIT} is not a bare repository."

def test_live_directory_exists():
    """Verify that the live directory exists."""
    assert os.path.isdir(LIVE_DIR), f"{LIVE_DIR} directory does not exist."

def test_hook_exists_and_executable():
    """Verify that the post-receive hook exists and is executable."""
    assert os.path.isfile(HOOK_PATH), f"Hook not found at {HOOK_PATH}."
    assert os.access(HOOK_PATH, os.X_OK), f"Hook at {HOOK_PATH} is not executable."

def test_socat_pid_and_process():
    """Verify socat.pid exists and points to a running socat process."""
    assert os.path.isfile(SOCAT_PID_FILE), f"{SOCAT_PID_FILE} does not exist."
    with open(SOCAT_PID_FILE, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"{SOCAT_PID_FILE} does not contain a valid PID."
    pid = int(pid_str)

    # Check if process exists and is socat
    try:
        cmdline_path = f"/proc/{pid}/cmdline"
        assert os.path.isfile(cmdline_path), f"Process with PID {pid} is not running."
        with open(cmdline_path, "r") as f:
            cmdline = f.read().replace('\x00', ' ')
        assert "socat" in cmdline, f"Process {pid} is not a socat process. Cmdline: {cmdline}"
    except Exception as e:
        pytest.fail(f"Failed to verify socat process: {e}")

def test_git_push_and_deployment():
    """Simulate a git push and verify that the hook deploys the code and starts the server."""
    test_string = "SUCCESS_DEPLOY_STRING_992_TEST"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize test repo
        subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)

        # Create a test file
        with open(os.path.join(tmpdir, "index.html"), "w") as f:
            f.write(test_string)

        # Commit and push
        subprocess.run(["git", "add", "index.html"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "remote", "add", "deploy", DEPLOY_GIT], cwd=tmpdir, check=True)

        # Push to deploy
        push_result = subprocess.run(["git", "push", "deploy", "master"], cwd=tmpdir, capture_output=True)
        assert push_result.returncode == 0, f"Git push failed: {push_result.stderr.decode()}"

        # Wait for the hook to finish starting the server
        time.sleep(2)

        # Check if file was deployed
        live_file = os.path.join(LIVE_DIR, "index.html")
        assert os.path.isfile(live_file), f"Deployed file not found at {live_file}."
        with open(live_file, "r") as f:
            content = f.read().strip()
        assert content == test_string, f"Deployed file content mismatch. Expected {test_string}, got {content}."

        # Check if HTTP server and socat proxy are working
        try:
            req = urllib.request.urlopen("http://localhost:8081/index.html", timeout=5)
            response = req.read().decode('utf-8').strip()
            assert response == test_string, f"HTTP response mismatch. Expected {test_string}, got {response}."
        except Exception as e:
            pytest.fail(f"Failed to access the deployed file via socat proxy on port 8081: {e}")

def test_server_log_exists():
    """Verify that the server.log file exists and has content."""
    assert os.path.isfile(SERVER_LOG), f"{SERVER_LOG} does not exist."
    assert os.path.getsize(SERVER_LOG) > 0, f"{SERVER_LOG} is empty."