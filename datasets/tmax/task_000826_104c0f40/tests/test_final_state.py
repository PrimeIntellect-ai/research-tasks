# test_final_state.py

import os
import subprocess
import glob
import urllib.request
import urllib.error
import json
import time

def test_validate_script_exists_and_executable():
    script_path = "/home/user/validate.sh"
    assert os.path.isfile(script_path), f"Validator script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Validator script is not executable: {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/validate.sh"
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run([script_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        res = subprocess.run([script_path, ef], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_config_updated():
    config_path = "/home/user/app/config.env"
    assert os.path.isfile(config_path), f"Config file missing: {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    assert "REDIS_PORT=6379" in content, "REDIS_PORT was not updated to 6379 in config.env"
    assert "VALIDATOR_SCRIPT=/home/user/validate.sh" in content, "VALIDATOR_SCRIPT was not set correctly in config.env"

def test_api_service_running_and_validates():
    # Give the service a moment to be fully up if it was just started
    time.sleep(1)

    url = "http://127.0.0.1:5000/ingest"

    # Test a clean payload
    clean_payload = json.dumps({"age": 25, "clicks": 10, "amount": 50.0}).encode('utf-8')
    req_clean = urllib.request.Request(url, data=clean_payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req_clean, timeout=5) as response:
            assert response.status in (200, 201, 202), f"Clean payload rejected by API, status: {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"API service is not reachable or rejected clean payload: {e}")

    # Test an evil payload
    evil_payload = json.dumps({"age": "25", "clicks": 10, "amount": 50.0}).encode('utf-8')
    req_evil = urllib.request.Request(url, data=evil_payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req_evil, timeout=5) as response:
            # If it succeeds, that's a failure (evil bypassed)
            pytest.fail("Evil payload was accepted by the API (expected HTTP error)")
    except urllib.error.HTTPError as e:
        # We expect a 4xx or 5xx error for invalid payloads
        assert e.code >= 400, f"Expected error code >= 400 for evil payload, got {e.code}"
    except urllib.error.URLError as e:
        # Connection refused might mean service is down, which is a failure, but we checked clean first
        pytest.fail(f"API service failed unexpectedly on evil payload: {e}")