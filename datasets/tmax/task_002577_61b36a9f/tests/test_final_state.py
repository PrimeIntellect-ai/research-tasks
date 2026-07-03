# test_final_state.py

import os
import stat
import subprocess
import urllib.request
import re
import pytest

def test_wrk_binary_compiled():
    wrk_path = "/app/wrk/wrk"
    assert os.path.isfile(wrk_path), f"wrk binary not found at {wrk_path}. Did you compile it?"
    assert os.access(wrk_path, os.X_OK), f"wrk binary at {wrk_path} is not executable."

def test_git_repo_and_hook():
    repo_path = "/home/user/git/api.git"
    assert os.path.isdir(repo_path), f"Bare git repository not found at {repo_path}."

    # Check if it's a bare repo
    result = subprocess.run(
        ["git", "rev-parse", "--is-bare-repository"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0 and result.stdout.strip() == "true", f"{repo_path} is not a valid bare Git repository."

    hook_path = os.path.join(repo_path, "hooks", "post-receive")
    assert os.path.isfile(hook_path), f"post-receive hook not found at {hook_path}."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"post-receive hook at {hook_path} is not executable."

def test_git_pushed():
    repo_path = "/home/user/git/api.git"
    result = subprocess.run(
        ["git", "log", "-1"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "No commits found in the bare repository. Did you push your changes?"

def test_docker_compose_and_tunnel():
    # Test Nginx directly on port 9090
    try:
        resp = urllib.request.urlopen("http://127.0.0.1:9090", timeout=3)
        assert resp.status == 200, f"Expected HTTP 200 from Nginx, got {resp.status}"
        body = resp.read().decode('utf-8')
        assert "OK" in body, "Expected 'OK' in response body from Nginx"
    except Exception as e:
        pytest.fail(f"Failed to access Nginx directly on port 9090. Is Docker Compose running and networks fixed? Error: {e}")

    # Test via SSH tunnel on port 8080
    try:
        resp = urllib.request.urlopen("http://127.0.0.1:8080", timeout=3)
        assert resp.status == 200, f"Expected HTTP 200 via SSH tunnel, got {resp.status}"
        body = resp.read().decode('utf-8')
        assert "OK" in body, "Expected 'OK' in response body via SSH tunnel"
    except Exception as e:
        pytest.fail(f"Failed to access API via SSH tunnel on port 8080. Is the tunnel running? Error: {e}")

def test_wrk_throughput():
    wrk_path = "/app/wrk/wrk"
    cmd = [wrk_path, "-t1", "-c10", "-d5s", "http://127.0.0.1:8080"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        pytest.fail("wrk load test timed out after 15 seconds.")

    assert result.returncode == 0, f"wrk failed to run. Stderr: {result.stderr}\nStdout: {result.stdout}"

    match = re.search(r"Requests/sec:\s+([0-9.]+)", result.stdout)
    assert match is not None, f"Could not parse 'Requests/sec' from wrk output:\n{result.stdout}"

    req_per_sec = float(match.group(1))
    threshold = 500.0
    assert req_per_sec >= threshold, f"Throughput metric failed: {req_per_sec} Requests/sec is strictly less than the required threshold of {threshold} Requests/sec."