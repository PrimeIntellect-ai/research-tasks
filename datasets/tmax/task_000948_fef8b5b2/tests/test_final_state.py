# test_final_state.py
import os
import subprocess
import requests
import tempfile
import shutil
import pytest

def test_venv_exists():
    """Check that the virtual environment was created properly."""
    venv_dir = "/home/user/venv"
    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} does not exist."
    assert os.path.isfile(os.path.join(venv_dir, "bin", "python")), "Python executable not found in the virtual environment."

def test_git_repo_and_hook():
    """Check that the bare git repository and executable post-receive hook exist."""
    repo_dir = "/home/user/target.git"
    assert os.path.isdir(repo_dir), f"Bare git repository {repo_dir} does not exist."
    assert os.path.isfile(os.path.join(repo_dir, "config")), f"{repo_dir} does not appear to be a valid git repository."

    hook_path = os.path.join(repo_dir, "hooks", "post-receive")
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def test_http_protocol_success():
    """Test that the daemon is accessible via the socat forwarder on port 9090 and accepts valid auth."""
    url = "http://127.0.0.1:9090/notify"
    headers = {"Authorization": "Bearer secure_admin_99"}
    data = {"event": "push"}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed. Is socat forwarding port 9090 to 8080, and is the daemon running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

def test_http_protocol_auth_failure():
    """Test that the daemon rejects invalid authorization tokens."""
    url = "http://127.0.0.1:9090/notify"
    headers = {"Authorization": "Bearer wrong_token"}
    data = {"event": "push"}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"HTTP request to {url} failed: {e}")

    assert response.status_code in (401, 403), f"Expected HTTP 401 or 403 for invalid token, got {response.status_code}. Response body: {response.text}"

def test_git_push_trigger():
    """Test that pushing to the git repository triggers the hook successfully."""
    repo_dir = "/home/user/target.git"
    clone_dir = tempfile.mkdtemp()
    try:
        # Clone the bare repository
        subprocess.run(["git", "clone", repo_dir, clone_dir], check=True, capture_output=True)

        # Create a test commit
        test_file = os.path.join(clone_dir, "test_trigger.txt")
        with open(test_file, "w") as f:
            f.write("Triggering the webhook via git push.\n")

        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)
        subprocess.run(["git", "add", "test_trigger.txt"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "test commit for webhook"], cwd=clone_dir, check=True)

        # Push to trigger the post-receive hook
        result = subprocess.run(["git", "push", "origin", "HEAD"], cwd=clone_dir, capture_output=True, text=True)

        assert result.returncode == 0, f"Git push failed, which likely means the post-receive hook failed. stderr: {result.stderr}"
    finally:
        shutil.rmtree(clone_dir)