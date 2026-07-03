# test_final_state.py

import os
import stat
import time
import urllib.request
import concurrent.futures
import pytest

def test_files_exist():
    assert os.path.isfile("/home/user/provision.py"), "/home/user/provision.py is missing"
    assert os.path.isfile("/home/user/rotate.py"), "/home/user/rotate.py is missing"
    assert os.path.isfile("/home/user/nginx.conf"), "/home/user/nginx.conf is missing"

def test_permissions():
    log_dir = "/home/user/proxy_logs"
    assert os.path.isdir(log_dir), f"{log_dir} is missing"

    dir_stat = os.stat(log_dir)
    assert oct(dir_stat.st_mode)[-3:] == '700', f"{log_dir} permissions must be 0700"

    log_file = os.path.join(log_dir, "access.log")
    if os.path.exists(log_file):
        file_stat = os.stat(log_file)
        assert oct(file_stat.st_mode)[-3:] == '600', f"{log_file} permissions must be 0600"

def fetch_url(url):
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read()
    except Exception:
        return None

def test_processes_running():
    # Check if backends are running on the required ports
    for port in [8001, 8002, 8003, 8004]:
        try:
            res = fetch_url(f"http://127.0.0.1:{port}/")
            assert res == b"OK", f"Backend on port {port} is not responding correctly"
        except Exception:
            pytest.fail(f"Backend on port {port} is not reachable")

def test_performance_metric():
    url = "http://127.0.0.1:8080/"

    # Send one request first to ensure Nginx is up and to create the log file if not created
    res = fetch_url(url)
    assert res == b"OK", "Nginx is not serving the backend correctly on port 8080"

    # Check log file permissions after a request
    log_file = "/home/user/proxy_logs/access.log"
    assert os.path.exists(log_file), f"{log_file} was not created after request"
    file_stat = os.stat(log_file)
    assert oct(file_stat.st_mode)[-3:] == '600', f"{log_file} permissions must be 0600"

    # Performance test: 200 concurrent requests
    start_time = time.time()
    success_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        futures = [executor.submit(fetch_url, url) for _ in range(200)]
        for future in concurrent.futures.as_completed(futures):
            if future.result() == b"OK":
                success_count += 1

    duration = time.time() - start_time
    assert success_count == 200, f"Expected 200 successful requests, got {success_count}"
    assert duration <= 3.5, f"Performance metric failed: took {duration:.2f}s, expected <= 3.5s"