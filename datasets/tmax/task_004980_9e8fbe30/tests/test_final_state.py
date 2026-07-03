# test_final_state.py

import os
import socket
import subprocess
import tempfile
import requests
import pytest

def test_start_services_script():
    """Test that the start_services.sh script exists and is executable."""
    script_path = "/home/user/start_services.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_web_service_valid_token():
    """Test the Web Service with the correct Authorization header."""
    url = "http://127.0.0.1:8181/"
    headers = {"Authorization": "Bearer AlphaX9"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
        assert response.text.strip() == "M1CRO_OK", f"Expected body 'M1CRO_OK', got '{response.text}'"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Web Service at {url}: {e}")

def test_web_service_invalid_token():
    """Test the Web Service with an invalid Authorization header."""
    url = "http://127.0.0.1:8181/"
    headers = {"Authorization": "Bearer WrongToken"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
        assert response.status_code == 401, f"Expected HTTP 401 for invalid token, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Web Service at {url}: {e}")

def test_web_service_no_token():
    """Test the Web Service with no Authorization header."""
    url = "http://127.0.0.1:8181/"
    try:
        response = requests.get(url, timeout=2)
        assert response.status_code == 401, f"Expected HTTP 401 for missing token, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Web Service at {url}: {e}")

def test_mock_ssh_service():
    """Test the Mock SSH Service."""
    host = "127.0.0.1"
    port = 3131
    try:
        with socket.create_connection((host, port), timeout=2) as s:
            data = s.recv(1024)
            assert data == b"SSH-2.0-RejectServer\r\n", f"Expected 'SSH-2.0-RejectServer\\r\\n', got {data}"

            # Check that the connection is closed
            data_after = s.recv(1024)
            assert data_after == b"", "Expected connection to be closed by server, but received more data."
    except Exception as e:
        pytest.fail(f"Failed to verify Mock SSH Service at {host}:{port}: {e}")

def test_git_hook_rejection():
    """Test that the git pre-receive hook rejects commits without 'APPROVED'."""
    repo_path = "/home/user/micro_repo.git"
    assert os.path.isdir(repo_path), f"Git repo {repo_path} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_cmd = ["git", "clone", repo_path, tmpdir]
        subprocess.run(clone_cmd, check=True, capture_output=True)

        # Create a commit without 'APPROVED'
        test_file = os.path.join(tmpdir, "test1.txt")
        with open(test_file, "w") as f:
            f.write("test")

        subprocess.run(["git", "add", "test1.txt"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Update files"], cwd=tmpdir, check=True, capture_output=True)

        # Push should fail
        push_result = subprocess.run(["git", "push"], cwd=tmpdir, capture_output=True)
        assert push_result.returncode != 0, "Push succeeded but was expected to fail because commit message lacked 'APPROVED'."

def test_git_hook_acceptance():
    """Test that the git pre-receive hook accepts commits with 'APPROVED'."""
    repo_path = "/home/user/micro_repo.git"
    assert os.path.isdir(repo_path), f"Git repo {repo_path} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_cmd = ["git", "clone", repo_path, tmpdir]
        subprocess.run(clone_cmd, check=True, capture_output=True)

        # Create a commit with 'APPROVED'
        test_file = os.path.join(tmpdir, "test2.txt")
        with open(test_file, "w") as f:
            f.write("test")

        subprocess.run(["git", "add", "test2.txt"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Update files APPROVED"], cwd=tmpdir, check=True, capture_output=True)

        # Push should succeed
        push_result = subprocess.run(["git", "push"], cwd=tmpdir, capture_output=True, text=True)
        assert push_result.returncode == 0, f"Push failed but was expected to succeed. Output: {push_result.stderr}"