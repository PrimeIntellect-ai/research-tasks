# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import subprocess
import glob
import re
import pytest

def test_solution_status():
    status_file = "/home/user/solution_status.txt"
    assert os.path.isfile(status_file), f"Solution status file missing at {status_file}"
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert "READY" in content, f"Expected 'READY' in {status_file}, found '{content}'"

def redis_lrange(key):
    try:
        result = subprocess.run(["redis-cli", "LRANGE", key, "0", "-1"], capture_output=True, text=True, check=True)
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Redis: {e.stderr}")

def clear_redis(key):
    subprocess.run(["redis-cli", "DEL", key], capture_output=True, check=True)

def post_to_service(payload):
    req = urllib.request.Request("http://127.0.0.1:8080/sanitize", data=payload, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.URLError as e:
        return getattr(e, 'code', str(e))

def test_clean_corpus():
    clean_dir = "/home/user/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    clear_redis("processed_logs")

    failed_files = []
    for filepath in clean_files:
        with open(filepath, "rb") as f:
            payload = f.read()

        status = post_to_service(payload)
        if status not in (200, 201, 202, 204):
            failed_files.append(os.path.basename(filepath))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(clean_files)} clean logs failed to POST: {failed_files}"

    logs = redis_lrange("processed_logs")
    assert len(logs) == len(clean_files), f"Expected {len(clean_files)} logs in Redis, found {len(logs)}"

    # We won't perfectly match order if async, but we can check if all original logs exist
    original_logs = []
    for filepath in clean_files:
        with open(filepath, "r") as f:
            original_logs.append(json.loads(f.read()))

    redis_logs = [json.loads(log) for log in logs]

    missing = []
    for orig in original_logs:
        if orig not in redis_logs:
            missing.append(orig)

    assert len(missing) == 0, f"{len(missing)} of {len(clean_files)} clean logs were modified or not found in Redis."

def test_evil_corpus():
    evil_dir = "/home/user/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    clear_redis("processed_logs")

    failed_files = []
    for filepath in evil_files:
        with open(filepath, "rb") as f:
            payload = f.read()

        status = post_to_service(payload)
        if status not in (200, 201, 202, 204):
            failed_files.append(os.path.basename(filepath))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(evil_files)} evil logs crashed or failed to POST: {failed_files}"

    logs = redis_lrange("processed_logs")
    assert len(logs) == len(evil_files), f"Expected {len(evil_files)} logs in Redis, found {len(logs)}"

    ssn_regex = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

    bypassed = 0
    for log_str in logs:
        try:
            log_obj = json.loads(log_str)
        except json.JSONDecodeError:
            bypassed += 1
            continue

        def check_pii(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in ("ssn", "credit_card") and v != "[REDACTED]":
                        return True
                    if check_pii(v):
                        return True
            elif isinstance(obj, list):
                for item in obj:
                    if check_pii(item):
                        return True
            elif isinstance(obj, str):
                if ssn_regex.search(obj) and obj != "[REDACTED]":
                    return True
            return False

        if check_pii(log_obj):
            bypassed += 1

    assert bypassed == 0, f"{bypassed} of {len(evil_files)} evil logs bypassed sanitization and contained PII."