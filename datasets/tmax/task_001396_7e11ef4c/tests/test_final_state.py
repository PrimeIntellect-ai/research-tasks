# test_final_state.py

import os
import glob
import subprocess
import json
import urllib.request
import urllib.error
import pytest

def test_filter_tz_script():
    # Find the filter script
    scripts = glob.glob("/home/user/filter_tz.*")
    assert scripts, "No filter_tz script found in /home/user/."

    # Assume the first one is the target if multiple exist, but prefer executable
    script_path = None
    for s in scripts:
        if os.access(s, os.X_OK):
            script_path = s
            break
    if not script_path:
        script_path = scripts[0]
        # If not executable, we might need to invoke it via interpreter, but we'll try to run it directly
        os.chmod(script_path, 0o755)

    evil_dir = "/home/user/corpora/tz_evil"
    clean_dir = "/home/user/corpora/tz_clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir)]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir)]

    evil_bypassed = []
    for f in evil_files:
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)

def test_fstab_setup():
    fstab_path = "/home/user/app_fstab"
    assert os.path.isfile(fstab_path), f"fstab file {fstab_path} is missing."
    with open(fstab_path, "r") as f:
        content = f.read()

    assert "/home/user/data_source" in content, "data_source not found in app_fstab."
    assert "/home/user/app/data" in content, "app/data not found in app_fstab."
    assert "bind" in content, "bind option not found in app_fstab."

def test_deploy_script_exists():
    deploy_path = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_path), f"Deployment script {deploy_path} is missing."

def test_backend_env_configured():
    env_path = "/home/user/app/config/backend.env"
    assert os.path.isfile(env_path), f"Environment file {env_path} is missing."
    with open(env_path, "r") as f:
        content = f.read()

    assert "REDIS_HOST=localhost" in content or "REDIS_HOST=127.0.0.1" in content, "REDIS_HOST not set correctly."
    assert "REDIS_PORT=6379" in content, "REDIS_PORT not set correctly."
    assert "LANG=en_US.UTF-8" in content, "LANG not set correctly."
    assert "TZ=UTC" in content, "TZ not set correctly."

def test_nginx_conf_configured():
    nginx_path = "/home/user/app/config/nginx.conf"
    assert os.path.isfile(nginx_path), f"NGINX config {nginx_path} is missing."
    with open(nginx_path, "r") as f:
        content = f.read()

    assert "5000" in content, "NGINX config does not seem to proxy to port 5000."

def test_end_to_end_health():
    # Attempt to hit the health endpoint
    url = "http://localhost:8080/api/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("status") == "ok", "Expected status 'ok'"
            assert data.get("redis") == "connected", "Expected redis 'connected'"
    except urllib.error.URLError as e:
        # If services aren't running, we fail the test
        pytest.fail(f"Failed to connect to {url}: {e}")