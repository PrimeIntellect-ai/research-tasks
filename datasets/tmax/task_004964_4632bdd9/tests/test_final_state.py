# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import pytest

def test_multiplier_file():
    path = "/home/user/img_service/multiplier.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you extract the multiplier and save it?"

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as a float in {path}.")

    assert abs(val - 42.5) < 0.01, f"Expected multiplier to be 42.5, got {val}"

def get_server_pid():
    for pid_str in os.listdir('/proc'):
        if not pid_str.isdigit():
            continue
        try:
            with open(f"/proc/{pid_str}/cmdline", "r") as f:
                cmdline = f.read().replace('\x00', ' ')
            if 'python' in cmdline and 'server.py' in cmdline:
                return int(pid_str)
        except Exception:
            continue
    return None

def get_memory_mb(pid):
    try:
        with open(f"/proc/{pid}/statm", "r") as f:
            rss_pages = int(f.read().split()[1])
        # Default page size is 4096 bytes
        return (rss_pages * 4096) / (1024 * 1024)
    except Exception as e:
        pytest.fail(f"Failed to read memory usage for PID {pid}: {e}")

def post_json(url, data):
    req = urllib.request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    json_data = json.dumps(data).encode("utf-8")
    try:
        with urllib.request.urlopen(req, data=json_data, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        pytest.fail(f"Request to {url} failed: {e}")

def test_server_correctness_and_memory_leak():
    pid = get_server_pid()
    assert pid is not None, "server.py is not running. Did you start the service?"

    url = 'http://127.0.0.1:8000/process'

    # 1. Check Numerical Correctness
    test_pixels = [200] * 1000
    payload = {"pixels": test_pixels, "multiplier": 42.5}

    resp_data = post_json(url, payload)
    assert "result" in resp_data, "Response JSON missing 'result' key."

    res = resp_data["result"]
    expected = 8500.0
    assert abs(res - expected) <= 1.0, f"Numerical correctness failed. Expected ~{expected}, got {res}. Integer overflow might still exist."

    # 2. Check Memory Leak
    mem_before = get_memory_mb(pid)

    # Load test
    for _ in range(5000):
        post_json(url, {"pixels": [100] * 50, "multiplier": 1.0})

    mem_after = get_memory_mb(pid)
    leaked_mb = mem_after - mem_before

    assert leaked_mb <= 5.0, f"Memory leak detected! Leaked {leaked_mb:.2f} MB during load test, which exceeds the 5.0 MB threshold."