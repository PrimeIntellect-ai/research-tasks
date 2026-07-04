# test_final_state.py

import os
import glob
import json
import socket
import requests
import pytest

def test_service_is_running():
    """Verify that the Flask receiver is listening on port 5000."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 5000))
        assert result == 0, "The Telemetry Receiver service is not listening on port 5000. Did you start the services?"

def test_adversarial_corpus_filtering():
    """Verify that the filter strictly accepts clean payloads and rejects evil payloads."""
    clean_files = glob.glob('/app/corpora/clean/*.json')
    evil_files = glob.glob('/app/corpora/evil/*.json')

    assert len(clean_files) > 0, "No clean payload files found in /app/corpora/clean/"
    assert len(evil_files) > 0, "No evil payload files found in /app/corpora/evil/"

    clean_failed = []
    for f in clean_files:
        with open(f, 'r') as file:
            data = json.load(file)
        try:
            res = requests.post('http://127.0.0.1:5000/telemetry', json=data, timeout=2)
            if res.status_code != 200:
                clean_failed.append(os.path.basename(f))
        except Exception:
            clean_failed.append(os.path.basename(f))

    evil_bypassed = []
    for f in evil_files:
        with open(f, 'r') as file:
            data = json.load(file)
        try:
            res = requests.post('http://127.0.0.1:5000/telemetry', json=data, timeout=2)
            if res.status_code == 200:
                evil_bypassed.append(os.path.basename(f))
        except Exception:
            # Request failed (e.g., connection drop or 500), which is an acceptable rejection
            pass

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_filter_script_exists_and_executable():
    """Verify that the telemetry filter script exists and is executable."""
    script_path = "/home/user/telemetry_filter.py"
    assert os.path.isfile(script_path), f"Filter script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Filter script {script_path} is not executable."