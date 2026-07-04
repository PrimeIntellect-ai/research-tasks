# test_final_state.py

import os
import time
import socket
import subprocess
import concurrent.futures
import pytest

PROXY_BIN = "/home/user/provision_cache_proxy"
GIT_DIR = "/home/user/config.git"
HOST = "127.0.0.1"
PORT = 8080
NUM_REQUESTS = 100
TARGET_TIME = 66.0  # seconds

def test_proxy_binary_exists():
    assert os.path.exists(PROXY_BIN), f"Proxy binary not found at {PROXY_BIN}"
    assert os.access(PROXY_BIN, os.X_OK), f"Proxy binary at {PROXY_BIN} is not executable"

def test_git_repo_exists():
    assert os.path.isdir(GIT_DIR), f"Bare Git repository not found at {GIT_DIR}"
    assert os.path.isdir(os.path.join(GIT_DIR, "objects")), f"{GIT_DIR} does not look like a bare Git repository"

def send_request():
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(b"/home/user/config.git\n")
            data = s.recv(4096)
            return data
    except Exception as e:
        return None

def test_proxy_performance():
    # Check if proxy is running, if not, start it
    proxy_proc = None
    try:
        with socket.create_connection((HOST, PORT), timeout=1):
            pass
    except OSError:
        # Start the proxy
        proxy_proc = subprocess.Popen([PROXY_BIN])
        time.sleep(2)  # Give it time to start

    try:
        # Warm-up request
        send_request()

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(send_request) for _ in range(NUM_REQUESTS)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        end_time = time.time()
        total_time = end_time - start_time

        successful_requests = [r for r in results if r is not None]
        assert len(successful_requests) == NUM_REQUESTS, f"Only {len(successful_requests)}/{NUM_REQUESTS} requests succeeded"

        assert total_time < TARGET_TIME, f"Performance test failed: took {total_time:.2f}s, target is < {TARGET_TIME}s. Speedup condition not met."
    finally:
        if proxy_proc is not None:
            proxy_proc.terminate()
            proxy_proc.wait()