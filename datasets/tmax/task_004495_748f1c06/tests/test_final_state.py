# test_final_state.py

import os
import struct
import socket
import time
import subprocess
import pytest
import requests
import json
import math

def test_recovered_csv():
    journal_path = "/app/data/journal.bin"
    recovered_path = "/app/data/recovered.csv"

    assert os.path.exists(journal_path), f"Missing {journal_path}"
    assert os.path.exists(recovered_path), f"Missing {recovered_path}"

    expected_floats = []
    with open(journal_path, "rb") as f:
        while True:
            chunk = f.read(16)
            if len(chunk) < 16:
                break

            magic, = struct.unpack("<I", chunk[0:4])
            if magic != 0xDEADBEEF:
                break

            val_float, = struct.unpack("<d", chunk[4:12])
            half1, half2 = struct.unpack("<II", chunk[4:12])
            expected_checksum = half1 ^ half2

            actual_checksum, = struct.unpack("<I", chunk[12:16])
            if actual_checksum != expected_checksum:
                break

            expected_floats.append(val_float)

    with open(recovered_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_floats), f"Expected {len(expected_floats)} lines in recovered.csv, got {len(lines)}"

    for i, (actual_str, expected_val) in enumerate(zip(lines, expected_floats)):
        expected_str = f"{expected_val:.6f}"
        assert actual_str == expected_str, f"Line {i+1} mismatch: expected {expected_str}, got {actual_str}"

def test_compute_endpoint_numerical_stability():
    url = "http://127.0.0.1:8080/compute"
    payload = {"data": [10000000000000000.0, 10000000000000001.0, 10000000000000002.0]}

    try:
        response = requests.post(url, json=payload, timeout=2.0)
    except requests.exceptions.Timeout:
        pytest.fail("Request timed out - the backend is likely in an infinite loop.")
    except requests.exceptions.ConnectionError:
        pytest.fail("Connection error - Nginx or backend is not running.")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Invalid JSON response: {response.text}")

    assert "variance" in data, f"Missing 'variance' in response: {data}"

    variance = data["variance"]
    assert math.isclose(variance, 1.0, rel_tol=1e-5), f"Expected variance ~1.0, got {variance}"

def get_backend_pid():
    try:
        # Try finding the process listening on 8081
        cmd = "lsof -t -i:8081"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        pids = result.stdout.strip().split()
        if pids:
            return int(pids[0])
    except Exception:
        pass

    try:
        # Fallback to pgrep
        cmd = "pgrep -f backend"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        pids = result.stdout.strip().split()
        if pids:
            return int(pids[0])
    except Exception:
        pass

    return None

def get_thread_count(pid):
    status_file = f"/proc/{pid}/status"
    if not os.path.exists(status_file):
        return None
    with open(status_file, "r") as f:
        for line in f:
            if line.startswith("Threads:"):
                return int(line.split()[1])
    return None

def test_thread_leak_on_disconnect():
    pid = get_backend_pid()
    assert pid is not None, "Could not find backend process running on port 8081"

    initial_threads = get_thread_count(pid)
    assert initial_threads is not None, "Could not read thread count"

    # Send 50 partial requests and drop connections
    for _ in range(50):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect(("127.0.0.1", 8080))
            s.sendall(b"POST /compute HTTP/1.1\r\nContent-Length: 900\r\n\r\n{\"data\": [")
            s.close()
        except Exception as e:
            pass

    # Wait a moment for threads to potentially clean up or leak
    time.sleep(1.0)

    final_threads = get_thread_count(pid)
    assert final_threads is not None, "Could not read thread count after test"

    assert final_threads < 20, f"Thread leak detected! Thread count is {final_threads} (initial was {initial_threads})"

def test_fuzz_test_exists_and_compiled():
    fuzz_src = "/app/src/fuzz_test.cpp"
    assert os.path.exists(fuzz_src), f"Missing fuzz test source: {fuzz_src}"

    with open(fuzz_src, "r") as f:
        content = f.read()

    assert "LLVMFuzzerTestOneInput" in content, f"Function LLVMFuzzerTestOneInput not found in {fuzz_src}"