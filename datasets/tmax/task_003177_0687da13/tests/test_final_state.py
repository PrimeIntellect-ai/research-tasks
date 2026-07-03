# test_final_state.py

import os
import time
import urllib.request
import json
import pytest

def test_backup_files_exist():
    backup_binary = "/home/user/backup/metrics_processor"
    backup_db = "/home/user/backup/metrics.db"

    assert os.path.isfile(backup_binary), f"Backup binary missing at {backup_binary}"
    assert os.path.isfile(backup_db), f"Backup DB missing at {backup_db}"

def test_deploy_expect_script_exists():
    expect_script = "/home/user/deploy.exp"
    assert os.path.isfile(expect_script), f"Expect script missing at {expect_script}"

def test_processor_latency_metric():
    """
    Test the latency of the optimized Rust metrics processor.
    Sends 50,000 log entries to port 8082 and measures response time.
    Threshold: latency <= 1.0 seconds.
    """
    url = "http://localhost:8082/process_batch"
    payload = json.dumps({"count": 50000}).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    req = urllib.request.Request(url, data=payload, headers=headers)

    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the Rust processor on port 8082: {e}")

    latency = time.time() - start_time

    assert status == 200, f"Expected HTTP 200, got {status}"
    assert latency <= 1.0, f"Latency {latency:.4f}s exceeds 1.0s threshold"
    print(f"LATENCY_METRIC: {latency}")