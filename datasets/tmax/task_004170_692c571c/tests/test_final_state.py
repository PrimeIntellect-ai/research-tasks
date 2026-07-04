# test_final_state.py

import os
import subprocess
import time
import random
import pytest

def generate_requests(filepath, num_requests=200000):
    ips = [f"192.168.1.{i}" for i in range(1, 255)] + [f"10.0.0.{i}" for i in range(1, 255)]
    methods = ["GET", "POST", "PUT", "DELETE"]
    paths = [
        "/api/v1/users", "/api/v1/login", "/api/v1/logout", "/api/v1/settings",
        "/api/v2/data", "/health", "/metrics", "/unknown/path", "/api/v1/secure"
    ]

    with open(filepath, 'w') as f:
        # Generate requests with some clustered timestamps to trigger rate limits
        current_time = 1600000000
        for i in range(num_requests):
            if random.random() < 0.2:
                current_time += 1
            ip = random.choice(ips)
            method = random.choice(methods)
            path = random.choice(paths)
            f.write(f"{current_time} {ip} {method} {path}\n")

def test_fast_waf_performance_and_accuracy():
    routes_conf = "/home/user/routes.conf"
    fast_waf = "/home/user/fast_waf"
    oracle = "/app/legacy_waf_oracle"
    requests_file = "/tmp/large_requests.txt"

    assert os.path.isfile(routes_conf), f"routes.conf is missing at {routes_conf}"
    assert os.path.isfile(fast_waf), f"fast_waf binary is missing at {fast_waf}"
    assert os.access(fast_waf, os.X_OK), f"fast_waf at {fast_waf} is not executable"

    # Generate test data
    generate_requests(requests_file, 200000)

    # Run oracle
    start_time = time.time()
    oracle_proc = subprocess.run(
        [oracle, routes_conf],
        stdin=open(requests_file, 'r'),
        capture_output=True,
        text=True
    )
    oracle_time = time.time() - start_time
    assert oracle_proc.returncode == 0, "Oracle failed to run"
    oracle_output = oracle_proc.stdout.strip().split('\n')

    # Run fast_waf
    start_time = time.time()
    fast_waf_proc = subprocess.run(
        [fast_waf, routes_conf],
        stdin=open(requests_file, 'r'),
        capture_output=True,
        text=True
    )
    fast_waf_time = time.time() - start_time
    assert fast_waf_proc.returncode == 0, "fast_waf failed to run"
    fast_waf_output = fast_waf_proc.stdout.strip().split('\n')

    # Calculate accuracy
    assert len(fast_waf_output) == len(oracle_output), f"Output length mismatch: expected {len(oracle_output)}, got {len(fast_waf_output)}"

    matches = sum(1 for o, f in zip(oracle_output, fast_waf_output) if o == f)
    accuracy = matches / len(oracle_output)

    # Calculate speedup
    speedup = oracle_time / fast_waf_time if fast_waf_time > 0 else float('inf')

    assert accuracy >= 0.999, f"Decision Accuracy={accuracy:.4f} is below threshold 0.999"
    assert speedup >= 1.5, f"Speedup={speedup:.2f}x is below threshold 1.5x (Oracle: {oracle_time:.4f}s, Fast WAF: {fast_waf_time:.4f}s)"