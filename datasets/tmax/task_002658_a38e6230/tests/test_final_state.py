# test_final_state.py

import os
import subprocess
import json
import urllib.request
import time
import glob

def test_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/app/filter/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer binary not found at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), "Sanitizer is not executable"

    evil_files = glob.glob("/home/user/corpora/evil/*")
    assert len(evil_files) > 0, "No files found in evil corpus"

    bypassed_files = []
    for f in evil_files:
        result = subprocess.run([sanitizer_path, f], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(f))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"

def test_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/app/filter/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer binary not found at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), "Sanitizer is not executable"

    clean_files = glob.glob("/home/user/corpora/clean/*")
    assert len(clean_files) > 0, "No files found in clean corpus"

    modified_files = []
    for f in clean_files:
        result = subprocess.run([sanitizer_path, f], capture_output=True)
        if result.returncode != 0:
            modified_files.append(os.path.basename(f))

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean modified/rejected: {', '.join(modified_files)}"

def test_nginx_config_updated():
    nginx_conf_path = "/home/user/app/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), "nginx.conf not found"
    with open(nginx_conf_path, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:9090;" in content, "nginx.conf does not route to 127.0.0.1:9090"

def test_backend_config_updated():
    backend_conf_path = "/home/user/app/backend/config.json"
    assert os.path.isfile(backend_conf_path), "config.json not found"
    with open(backend_conf_path, "r") as f:
        config = json.load(f)
    assert config.get("redis_port") == 6379, "Backend config.json does not point to redis port 6379"

def test_end_to_end_flow():
    # Send request to Nginx
    url = "http://localhost:8080/api/submit"
    data = b"clean data"
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except Exception as e:
        assert False, f"Failed to send request to nginx: {e}"

    # Check redis
    try:
        result = subprocess.run(["redis-cli", "GET", "last_payload"], capture_output=True, text=True, check=True)
        assert "clean data" in result.stdout, "Redis did not contain the expected 'last_payload'"
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to query redis: {e}"

def test_health_monitor_script():
    monitor_path = "/home/user/app/health_monitor.sh"
    assert os.path.isfile(monitor_path), f"{monitor_path} not found"
    assert os.access(monitor_path, os.X_OK), f"{monitor_path} is not executable"

    # Kill nginx
    subprocess.run(["pkill", "-f", "nginx"], capture_output=True)
    time.sleep(1)

    # Run health monitor
    subprocess.run([monitor_path], capture_output=True)
    time.sleep(2)

    # Check if nginx is back
    result = subprocess.run(["pgrep", "-f", "nginx"], capture_output=True)
    assert result.returncode == 0, "Nginx did not restart after running health_monitor.sh"