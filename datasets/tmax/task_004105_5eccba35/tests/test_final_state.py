# test_final_state.py
import os
import re
import subprocess
import time
import urllib.request
import urllib.error
import concurrent.futures
import pytest

APP_DIR = "/home/user/app"
MONITOR_SH = os.path.join(APP_DIR, "monitor.sh")
BACKEND_ARM = os.path.join(APP_DIR, "backend_arm")

def test_monitor_script_exists():
    assert os.path.isfile(MONITOR_SH), f"Monitor script {MONITOR_SH} does not exist."
    assert os.access(MONITOR_SH, os.X_OK) or "bash" in open(MONITOR_SH).read() or "sh" in open(MONITOR_SH).read(), \
        f"Monitor script {MONITOR_SH} should be executable or contain shell commands."

def test_backend_compiled():
    assert os.path.isfile(BACKEND_ARM), f"Compiled backend {BACKEND_ARM} does not exist."
    # Check if it's an ARM binary
    output = subprocess.check_output(["file", BACKEND_ARM]).decode()
    assert "ARM" in output or "aarch64" in output, f"{BACKEND_ARM} is not compiled for ARM/aarch64."

def test_services_running():
    # Check if Nginx is running
    pgrep_nginx = subprocess.run(["pgrep", "-f", "nginx"], capture_output=True)
    assert pgrep_nginx.returncode == 0, "Nginx is not running."

    # Check if QEMU backend is running
    pgrep_qemu = subprocess.run(["pgrep", "-f", "qemu-aarch64-static.*backend_arm"], capture_output=True)
    assert pgrep_qemu.returncode == 0, "Backend is not running via qemu-aarch64-static."

def test_basic_request():
    max_retries = 5
    for _ in range(max_retries):
        try:
            req = urllib.request.Request("http://127.0.0.1:8080/")
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200, f"Expected HTTP 200, got {response.status}"
                body = response.read().decode()
                assert "OK" in body, "Response body did not contain 'OK'"
                return
        except urllib.error.URLError as e:
            time.sleep(1)
    pytest.fail("Failed to connect to Nginx on 127.0.0.1:8080 or received bad response.")

def test_throughput_metric():
    # Attempt to use wrk as specified in the verifier details
    try:
        cmd = ["wrk", "-c", "20", "-d", "5s", "http://127.0.0.1:8080/"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        match = re.search(r"Requests/sec:\s+([\d\.]+)", result.stdout)
        if match:
            req_per_sec = float(match.group(1))
            assert req_per_sec >= 500.0, f"Throughput too low: {req_per_sec} req/sec (Threshold: 500.0). Did you remove the sleep(1) delay?"
            return
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass # Fallback to python-based load test if wrk is missing or fails

    # Fallback Python load test
    def fetch():
        try:
            with urllib.request.urlopen("http://127.0.0.1:8080/", timeout=2) as response:
                return response.status == 200
        except Exception:
            return False

    start_time = time.time()
    success_count = 0
    total_requests = 200

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch) for _ in range(total_requests)]
        for f in concurrent.futures.as_completed(futures):
            if f.result():
                success_count += 1

    duration = time.time() - start_time
    req_per_sec = success_count / duration

    # The python fallback is much slower than wrk, so we adjust the threshold for the fallback
    # If sleep(1) is present, throughput will be ~1-20 req/sec. Without it, it should easily exceed 100.
    assert req_per_sec >= 100.0, f"Throughput too low: {req_per_sec:.2f} req/sec (Fallback Threshold: 100.0). Did you remove the sleep(1) delay?"