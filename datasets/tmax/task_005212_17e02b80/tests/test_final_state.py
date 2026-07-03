# test_final_state.py

import os
import subprocess
import requests
import json
import pytest

VALIDATOR_PATH = "/home/user/validator.py"
CLEAN_DIR = "/app/tests/hidden_clean/"
EVIL_DIR = "/app/tests/hidden_evil/"

def test_validator_exists():
    assert os.path.isfile(VALIDATOR_PATH), f"Validator script missing at {VALIDATOR_PATH}"

def test_validator_clean_corpus():
    if not os.path.isdir(CLEAN_DIR):
        pytest.skip(f"Clean corpus directory missing at {CLEAN_DIR}")

    failed_files = []
    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    for f in files:
        filepath = os.path.join(CLEAN_DIR, f)
        result = subprocess.run(["python3", VALIDATOR_PATH, filepath], capture_output=True, text=True)
        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            failed_files.append(f)

    assert not failed_files, f"{len(failed_files)} of {len(files)} clean files were rejected or failed: {failed_files[:10]}"

def test_validator_evil_corpus():
    if not os.path.isdir(EVIL_DIR):
        pytest.skip(f"Evil corpus directory missing at {EVIL_DIR}")

    failed_files = []
    files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    for f in files:
        filepath = os.path.join(EVIL_DIR, f)
        result = subprocess.run(["python3", VALIDATOR_PATH, filepath], capture_output=True, text=True)
        if result.returncode != 1 or "REJECT" not in result.stdout:
            failed_files.append(f)

    assert not failed_files, f"{len(failed_files)} of {len(files)} evil files bypassed validation: {failed_files[:10]}"

def test_end_to_end_api_clean():
    if not os.path.isdir(CLEAN_DIR):
        pytest.skip(f"Clean corpus directory missing at {CLEAN_DIR}")

    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    if not files:
        pytest.skip("No clean files found to test API")

    test_file = os.path.join(CLEAN_DIR, files[0])
    with open(test_file, 'r') as f:
        payload = json.load(f)

    try:
        resp = requests.post("http://localhost:8001/ingest", json=payload, timeout=5)
        assert resp.status_code in [200, 201, 202], f"Expected success status code for clean payload, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API on port 8001: {e}")

def test_end_to_end_api_evil():
    if not os.path.isdir(EVIL_DIR):
        pytest.skip(f"Evil corpus directory missing at {EVIL_DIR}")

    files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    if not files:
        pytest.skip("No evil files found to test API")

    test_file = os.path.join(EVIL_DIR, files[0])
    with open(test_file, 'r') as f:
        payload = json.load(f)

    try:
        resp = requests.post("http://localhost:8001/ingest", json=payload, timeout=5)
        assert resp.status_code == 400, f"Expected 400 Bad Request for evil payload, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API on port 8001: {e}")