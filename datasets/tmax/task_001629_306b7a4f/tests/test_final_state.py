# test_final_state.py

import os
import subprocess
import json
import urllib.request
import urllib.error
import shutil
import tempfile
import pytest

def test_telemetry_stack_flow():
    # Send a POST request to the Nginx reverse proxy
    url = "http://localhost:8080/api/record"
    test_payload = {"test_key": "test_value", "timestamp": "2024-05-15T12:00:00Z"}
    data = json.dumps(test_payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status in (200, 201), f"Expected successful HTTP status, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx or Flask via {url}: {e}")

    # Check if the record was written to Redis using redis-cli
    try:
        # Assuming the Flask app stores the payload in some way. If we don't know the exact key,
        # we can check if the number of keys increased or if 'test_key' is present.
        # Since the task description says "save the record to Redis", let's check if the keyspace is non-empty
        # or just verify the HTTP success if we can't reliably guess the key. 
        # We will check if redis-cli works and has keys.
        redis_check = subprocess.run(
            ["redis-cli", "-p", "6379", "DBSIZE"],
            capture_output=True, text=True, check=True
        )
        dbsize = int(redis_check.stdout.strip().split()[-1])
        assert dbsize > 0, "Redis DBSIZE is 0. The record was not saved to Redis."
    except Exception as e:
        pytest.fail(f"Failed to verify Redis state: {e}")

def test_finops_cleaner_script():
    script_path = "/home/user/app/finops_cleaner.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    evil_corpus = "/home/user/tests/evil_corpus"
    clean_corpus = "/home/user/tests/clean_corpus"

    assert os.path.isdir(evil_corpus), f"Evil corpus directory {evil_corpus} is missing."
    assert os.path.isdir(clean_corpus), f"Clean corpus directory {clean_corpus} is missing."

    # Record initial files
    initial_evil_files = set(os.listdir(evil_corpus))
    initial_clean_files = set(os.listdir(clean_corpus))

    # Run script on evil corpus
    try:
        subprocess.run(["python3", script_path, evil_corpus], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed on evil corpus: {e.stderr}")

    # Run script on clean corpus
    try:
        subprocess.run(["python3", script_path, clean_corpus], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed on clean corpus: {e.stderr}")

    # Check results
    remaining_evil_files = set(os.listdir(evil_corpus))
    remaining_clean_files = set(os.listdir(clean_corpus))

    evil_bypassed = remaining_evil_files.intersection(initial_evil_files)
    clean_modified = initial_clean_files - remaining_clean_files

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(initial_evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(initial_clean_files)} clean modified (deleted): {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_cron_job_scheduled():
    try:
        crontab_out = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. No crontab for user?")

    # Look for the expected cron job
    # 0 2 * * * python3 /home/user/app/finops_cleaner.py /home/user/production_logs
    valid_cron_found = False
    for line in crontab_out.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            command = " ".join(parts[5:])
            if schedule == "0 2 * * *" and "finops_cleaner.py" in command and "/home/user/production_logs" in command:
                valid_cron_found = True
                break

    assert valid_cron_found, "Cron job for finops_cleaner.py at 2:00 AM is missing or incorrect."