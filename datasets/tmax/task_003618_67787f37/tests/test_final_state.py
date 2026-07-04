# test_final_state.py

import os
import glob
import subprocess
import urllib.request
import time
import pytest

def test_multi_service_end_to_end():
    # Clear the redis list first to ensure a clean slate
    subprocess.run(["redis-cli", "DEL", "latency_metrics"], capture_output=True)

    # Send 10 requests to the load balancer
    success_count = 0
    for _ in range(10):
        try:
            req = urllib.request.Request("http://127.0.0.1:8080/ping")
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    success_count += 1
        except Exception as e:
            pass
        time.sleep(0.1)

    assert success_count == 10, f"Expected 10 successful requests to Nginx, got {success_count}"

    # Check redis list length
    result = subprocess.run(["redis-cli", "LLEN", "latency_metrics"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to execute redis-cli"

    llen = int(result.stdout.strip())
    assert llen >= 10, f"Expected at least 10 items in 'latency_metrics' Redis list, found {llen}"

def test_adversarial_corpus_classifier():
    script_path = "/home/user/profile_classifier.py"
    assert os.path.isfile(script_path), f"Classifier script {script_path} does not exist"

    clean_dir = "/home/user/data/clean"
    evil_dir = "/home/user/data/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified (expected exit 0, got otherwise): {', '.join(failed_clean[:5])}...")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed (expected exit 1, got otherwise): {', '.join(failed_evil[:5])}...")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))