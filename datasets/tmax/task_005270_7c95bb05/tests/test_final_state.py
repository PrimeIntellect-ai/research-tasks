# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_filter_script_exists():
    assert os.path.exists("/home/user/filter.py"), "filter.py script is missing"

def test_filter_script_classification():
    clean_dir = "/home/user/data/clean"
    evil_dir = "/home/user/data/evil"
    script_path = "/home/user/filter.py"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.h5')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.h5')]

    clean_failed = []
    evil_failed = []

    for fpath in clean_files:
        try:
            res = subprocess.run(["python3", script_path, fpath], capture_output=True, text=True, check=True)
            if res.stdout.strip() != "ACCEPT":
                clean_failed.append(os.path.basename(fpath))
        except subprocess.CalledProcessError:
            clean_failed.append(os.path.basename(fpath))

    for fpath in evil_files:
        try:
            res = subprocess.run(["python3", script_path, fpath], capture_output=True, text=True, check=True)
            if res.stdout.strip() != "REJECT":
                evil_failed.append(os.path.basename(fpath))
        except subprocess.CalledProcessError:
            evil_failed.append(os.path.basename(fpath))

    err_msgs = []
    if evil_failed:
        err_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        err_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    if err_msgs:
        pytest.fail(" | ".join(err_msgs))

def test_nginx_config_fixed():
    nginx_conf = "/home/user/config/nginx.conf"
    assert os.path.exists(nginx_conf), "nginx.conf is missing"

    with open(nginx_conf, 'r') as f:
        content = f.read()

    assert "proxy_pass http://localhost:5000" in content or "proxy_pass http://127.0.0.1:5000" in content, \
        "nginx.conf does not route /api/upload to port 5000"
    assert "proxy_pass http://localhost:5001" in content or "proxy_pass http://127.0.0.1:5001" in content, \
        "nginx.conf does not route /api/align to port 5001"

def test_env_config_fixed():
    env_file = "/home/user/config/.env"
    assert os.path.exists(env_file), ".env is missing"

    with open(env_file, 'r') as f:
        content = f.read()

    assert "REDIS_PORT=6379" in content, ".env does not contain REDIS_PORT=6379"

def test_services_running():
    # Test align status
    try:
        req = urllib.request.Request("http://localhost:8080/api/align/status")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, "Align status endpoint did not return HTTP 200"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to align status endpoint: {e}")

    # Test upload endpoint
    try:
        req = urllib.request.Request("http://localhost:8080/api/upload", data=b"dummy", method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, "Upload endpoint did not return HTTP 200"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to upload endpoint: {e}")