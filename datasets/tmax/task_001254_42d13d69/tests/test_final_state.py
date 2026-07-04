# test_final_state.py

import os
import subprocess
import urllib.request
import time
import pytest

def test_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer.sh"
    assert os.path.isfile(sanitizer_path), f"Sanitizer script not found at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer script at {sanitizer_path} is not executable"

    clean_dir = "/home/user/data/clean"
    evil_dir = "/home/user/data/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean CSV files found."
    assert len(evil_files) > 0, "No evil CSV files found."

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run(["bash", sanitizer_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run(["bash", sanitizer_path, ef], capture_output=True)
        if res.returncode == 0:
            evil_failed.append(os.path.basename(ef))

    err_msg = []
    if evil_failed:
        err_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        err_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean rejected: {', '.join(clean_failed)}")

    if err_msg:
        pytest.fail(" | ".join(err_msg))

def test_multi_service_pipeline():
    # Ensure services are started
    start_script = "/home/user/app/start_services.sh"
    if os.path.exists(start_script):
        subprocess.run(["bash", start_script], check=False)
        time.sleep(3)  # Give services a moment to spin up

    # Send a valid CSV to the Nginx proxy
    csv_data = b"col1,col2,col3,experiment_id\n1,2,3,42\n"
    req = urllib.request.Request("http://localhost:8080/api/upload", data=csv_data, method="POST")
    req.add_header("Content-Type", "text/csv")

    try:
        response = urllib.request.urlopen(req, timeout=5)
        assert response.status in (200, 201), f"Expected successful HTTP status, got {response.status}"
    except Exception as e:
        pytest.fail(f"End-to-end flow failed at Nginx/Flask layer: {e}. Check if Nginx routes /api/ to Flask.")

    # Verify Redis uploads_count
    try:
        res = subprocess.run(["redis-cli", "get", "uploads_count"], capture_output=True, text=True, timeout=5)
        assert res.returncode == 0, "Failed to execute redis-cli"

        count_str = res.stdout.strip()
        assert count_str and count_str.isdigit(), f"Expected an integer in Redis for 'uploads_count', got: '{count_str}'"
        assert int(count_str) > 0, "Redis uploads_count was not incremented, meaning the Flask app didn't process the upload correctly."
    except Exception as e:
        pytest.fail(f"End-to-end flow failed at Redis layer: {e}")