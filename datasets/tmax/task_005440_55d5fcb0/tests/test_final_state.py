# test_final_state.py

import os
import socket
import threading
import subprocess
import time
import pytest

def test_provision_script_exists():
    """Test that the provision.sh script exists."""
    assert os.path.isfile("/home/user/provision.sh"), "provision.sh is missing"

def test_mail_env_exists():
    """Test that .mail_env exists and contains the required variables."""
    env_file = "/home/user/.mail_env"
    assert os.path.isfile(env_file), ".mail_env is missing"
    with open(env_file, "r") as f:
        content = f.read()
    assert "CLUSTER_NAME=alpha_cluster" in content, "CLUSTER_NAME is not set correctly in .mail_env"
    assert "WORKER_TIMEOUT=15" in content, "WORKER_TIMEOUT is not set correctly in .mail_env"

def test_haproxy_cfg_exists():
    """Test that haproxy.cfg was generated."""
    assert os.path.isfile("/home/user/haproxy.cfg"), "haproxy.cfg is missing"

def test_health_check_script():
    """Test that health_check.sh exists, is executable, and succeeds."""
    script_path = "/home/user/health_check.sh"
    assert os.path.isfile(script_path), "health_check.sh is missing"
    assert os.access(script_path, os.X_OK), "health_check.sh is not executable"

    # Run the health check script
    result = subprocess.run(["bash", script_path], capture_output=True)
    assert result.returncode == 0, f"health_check.sh failed with exit code {result.returncode}"

def test_benchmark_success_rate():
    """Benchmark the HAProxy load balancer to ensure high concurrency success rate."""
    SUCCESS_COUNT = 0
    TOTAL_REQUESTS = 5000
    lock = threading.Lock()

    def attack():
        nonlocal SUCCESS_COUNT
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect(('127.0.0.1', 2525))
            s.sendall(b"EHLO benchmark\r\n")
            data = s.recv(1024)
            if b"250" in data:
                with lock:
                    SUCCESS_COUNT += 1
            s.close()
        except Exception:
            pass

    threads = []
    for _ in range(TOTAL_REQUESTS):
        t = threading.Thread(target=attack)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success_rate = SUCCESS_COUNT / TOTAL_REQUESTS
    assert success_rate >= 0.99, f"Throughput test failed. Expected >= 0.99, got {success_rate} ({SUCCESS_COUNT}/{TOTAL_REQUESTS} successful)"