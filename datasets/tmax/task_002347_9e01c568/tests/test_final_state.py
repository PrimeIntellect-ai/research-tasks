# test_final_state.py
import os
import subprocess
import socket
import pytest

def test_limits_registered():
    path = "/home/user/.limits_registered"
    assert os.path.isfile(path), f"File {path} not found. Did the Expect script run successfully?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected 'SUCCESS' in {path}, got '{content}'"

def test_sanitiser_corpus():
    sanitiser_path = "/home/user/sanitiser"
    assert os.path.isfile(sanitiser_path), f"Sanitiser executable not found at {sanitiser_path}"
    assert os.access(sanitiser_path, os.X_OK), f"Sanitiser at {sanitiser_path} is not executable"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_failed = []
    for root, _, files in os.walk(clean_dir):
        for file in files:
            filepath = os.path.join(root, file)
            res = subprocess.run([sanitiser_path, filepath], capture_output=True)
            if res.returncode != 0:
                clean_failed.append(file)

    evil_failed = []
    for root, _, files in os.walk(evil_dir):
        for file in files:
            filepath = os.path.join(root, file)
            res = subprocess.run([sanitiser_path, filepath], capture_output=True)
            if res.returncode == 0:
                evil_failed.append(file)

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} clean files rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} evil files bypassed: {', '.join(evil_failed)}")

    assert not errors, " | ".join(errors)

def test_git_repo_and_hook():
    repo_dir = "/home/user/metrics.git"
    assert os.path.isdir(repo_dir), f"Git repo directory {repo_dir} not found"

    config_path = os.path.join(repo_dir, "config")
    assert os.path.isfile(config_path), f"Git config not found at {config_path}"

    with open(config_path, "r") as f:
        config_content = f.read()
    assert "bare = true" in config_content.lower() or "bare = true" in config_content.replace(" ", "").lower(), "Git repository is not bare"

    hook_path = os.path.join(repo_dir, "hooks", "pre-receive")
    assert os.path.isfile(hook_path), f"pre-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"pre-receive hook at {hook_path} is not executable"

def test_nginx_setup():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config not found at {conf_path}"

    with open(conf_path, "r") as f:
        conf_content = f.read()

    assert "8081" in conf_content and "8082" in conf_content, "Nginx config missing upstream servers 8081 and 8082"
    assert "8080" in conf_content, "Nginx config missing listen port 8080"

    # Check if nginx is running and listening on 8080
    try:
        with socket.create_connection(("127.0.0.1", 8080), timeout=2):
            pass
    except OSError:
        pytest.fail("Nginx is not listening on port 8080. Is the service running?")