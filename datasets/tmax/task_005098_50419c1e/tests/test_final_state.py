# test_final_state.py

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
import pytest

SCRIPT_PATH = "/home/user/sanitiser.py"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def get_redis_ingest_count():
    try:
        # Using redis-cli since redis-py might not be in the environment, though it's likely installed.
        # Let's try redis-cli
        result = subprocess.run(["redis-cli", "GET", "ingest_count"], capture_output=True, text=True, check=True)
        val = result.stdout.strip()
        if val == "(nil)" or not val:
            return 0
        # redis-cli might output "10" or (nil)
        # remove quotes if any
        val = val.replace('"', '')
        return int(val)
    except Exception:
        return 0

def test_sanitiser_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Sanitiser script not found at {SCRIPT_PATH}"

def test_services_running():
    # Test Nginx -> Flask -> Redis flow by making a direct request to Nginx
    # We will send a dummy valid payload to Nginx
    req = urllib.request.Request(
        "http://localhost:8080/ingest",
        data=json.dumps({"dummy": "data"}).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, "Expected HTTP 200 from Nginx/Flask"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or Flask on 5000: {e}")

def test_clean_corpus():
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found."

    initial_count = get_redis_ingest_count()
    failed_files = []

    for fpath in clean_files:
        result = subprocess.run([sys.executable, SCRIPT_PATH, fpath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(fpath))

    final_count = get_redis_ingest_count()
    ingested = final_count - initial_count

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files were rejected (exit code != 0). Offending files: {', '.join(failed_files[:5])}..."
    assert ingested == len(clean_files), f"Expected {len(clean_files)} ingestions in Redis, but got {ingested}."

def test_evil_corpus():
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found."

    initial_count = get_redis_ingest_count()
    bypassed_files = []

    for fpath in evil_files:
        result = subprocess.run([sys.executable, SCRIPT_PATH, fpath], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(fpath))

    final_count = get_redis_ingest_count()
    ingested = final_count - initial_count

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed validation (exit code 0). Offending files: {', '.join(bypassed_files[:5])}..."
    assert ingested == 0, f"Expected 0 ingestions in Redis for evil files, but got {ingested}."