# test_final_state.py
import os
import stat
import subprocess
import requests
import pytest

def test_git_repo_setup():
    """Verify the git repository and post-receive hook."""
    repo_path = "/home/user/operator.git"
    assert os.path.isdir(os.path.join(repo_path, "objects")), f"{repo_path} is not a bare git repository"

    hook_path = os.path.join(repo_path, "hooks/post-receive")
    assert os.path.isfile(hook_path), f"post-receive hook missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-receive hook at {hook_path} is not executable"

    with open(hook_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"post-receive hook at {hook_path} is not a compiled ELF executable"

def test_crontab_setup():
    """Verify the health check script and crontab."""
    script_path = "/home/user/health.sh"
    assert os.path.isfile(script_path), f"Health check script missing at {script_path}"

    try:
        output = subprocess.check_output(["crontab", "-l"], text=True)
        assert script_path in output, f"{script_path} not found in user crontab"
    except subprocess.CalledProcessError:
        pytest.fail("crontab command failed or no crontab configured for user")

def test_git_push_and_http_server():
    """Simulate a git push and verify the hook execution and HTTP server response."""
    test_repo = "/tmp/test-repo"
    subprocess.run(["rm", "-rf", test_repo], check=False)

    # Clone the repo
    clone_proc = subprocess.run(["git", "clone", "/home/user/operator.git", test_repo], capture_output=True, text=True)
    assert clone_proc.returncode == 0, f"Failed to clone repository: {clone_proc.stderr}"

    # Create and push a CRD
    crd_path = os.path.join(test_repo, "deployment.crd")
    with open(crd_path, "w") as f:
        f.write("kind: CustomDeployment\n")

    subprocess.run(["git", "-C", test_repo, "add", "deployment.crd"], check=True)
    subprocess.run(["git", "-C", test_repo, "commit", "-m", "Test CRD"], check=True)

    push_proc = subprocess.run(["git", "-C", test_repo, "push", "origin", "master"], capture_output=True, text=True)
    assert push_proc.returncode == 0, f"Git push failed: {push_proc.stderr}"

    # Verify file state
    deployment_json = "/home/user/webroot/deployment.json"
    latest_json = "/home/user/webroot/latest.json"

    assert os.path.isfile(deployment_json), f"Expected {deployment_json} to be created by the hook"

    st = os.stat(deployment_json)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o600, f"Expected permissions 0600 for {deployment_json}, got {oct(mode)}"

    assert os.path.islink(latest_json), f"{latest_json} must be a symlink"
    target = os.readlink(latest_json)
    # Target could be absolute or relative
    if not os.path.isabs(target):
        target = os.path.abspath(os.path.join(os.path.dirname(latest_json), target))
    assert target == deployment_json, f"Symlink {latest_json} does not point to {deployment_json}"

    # Verify HTTP server
    try:
        resp = requests.get("http://127.0.0.1:8080/api/v1/manifest", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}"

    content_type = resp.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type: application/json, got {content_type}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("status") == "parsed", f"JSON response does not match expected output from crd_parser: {data}"