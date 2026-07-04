# test_final_state.py

import time
import urllib.request
import concurrent.futures
import numpy as np
import pytest
import os
import json

def fetch(url):
    start = time.perf_counter()
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
            status = response.status
    except Exception:
        status = 500
    return time.perf_counter() - start, status

def test_latency_and_correctness():
    url = "http://127.0.0.1:8080/export?customer_id=CUST_123"

    times = []
    statuses = []

    # Run 500 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(fetch, url) for _ in range(500)]
        for future in concurrent.futures.as_completed(futures):
            t, s = future.result()
            times.append(t)
            statuses.append(s)

    success_count = sum(1 for s in statuses if s == 200)
    assert success_count == 500, f"Expected 500 successful requests, got {success_count}. Is the service running and handling load?"

    p95 = np.percentile(times, 95)

    results_file = "/home/user/results.ndjson"
    assert os.path.exists(results_file), f"Results file {results_file} does not exist. Did the service write the output?"

    with open(results_file, "r") as f:
        lines = f.readlines()
        assert len(lines) > 0, "Results file is empty."
        last_line = lines[-1].strip()
        try:
            data = json.loads(last_line)
            assert "category" in data, "Missing 'category' in result JSON."
            assert "total_spent" in data, "Missing 'total_spent' in result JSON."
        except json.JSONDecodeError:
            pytest.fail(f"Last line of {results_file} is not valid JSON: {last_line}")

    assert p95 <= 0.250, f"P95 latency is {p95:.4f}s, which is greater than the threshold of 0.250s. The query is not optimized enough."