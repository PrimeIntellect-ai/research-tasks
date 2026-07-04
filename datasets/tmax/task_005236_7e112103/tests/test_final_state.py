# test_final_state.py

import os
import stat
import urllib.request
import urllib.error

def test_result_log_content():
    """Verify that result.log exists and contains the exact string."""
    log_path = "/home/user/result.log"
    assert os.path.exists(log_path), f"File not found: {log_path}"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "MICROSERVICE_V1_ACTIVE", f"Incorrect content in {log_path}: {content}"

def test_service_running_and_responding():
    """Verify that the microservice is running on port 8282 and responds correctly."""
    url = "http://localhost:8282/"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8').strip()
            assert body == "MICROSERVICE_V1_ACTIVE", f"Incorrect response from service: {body}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to service at {url}: {e}"

def test_git_hook_executable():
    """Verify that the post-receive hook exists and is executable."""
    hook_path = "/home/user/app.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"Hook not found: {hook_path}"

    st = os.stat(hook_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Hook is not executable: {hook_path}"

def test_bare_git_repo():
    """Verify that app.git is a bare git repository."""
    repo_path = "/home/user/app.git"
    assert os.path.isdir(repo_path), f"Repo directory not found: {repo_path}"

    config_path = os.path.join(repo_path, "config")
    assert os.path.exists(config_path), f"Git config not found in {repo_path}"

    with open(config_path, "r") as f:
        config_content = f.read()

    assert "bare = true" in config_content.lower(), f"Repository at {repo_path} is not configured as bare."

def test_env_sh_exists():
    """Verify that env.sh exists and contains the expected export."""
    env_path = "/home/user/env.sh"
    assert os.path.exists(env_path), f"Environment file not found: {env_path}"
    with open(env_path, "r") as f:
        content = f.read()
    assert "APP_PORT=8282" in content, f"APP_PORT=8282 not found in {env_path}"