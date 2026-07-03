# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import pytest

EVIL_DIR = "/home/user/app/corpora/evil"
CLEAN_DIR = "/home/user/app/corpora/clean"
URL = "http://127.0.0.1:8080/api/execute"

def send_request(payload):
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return 0  # Connection error or timeout

def test_server_is_up():
    """Ensure Nginx and the backend are reachable before running corpus tests."""
    status = send_request({"hex_code": "90"})
    if status == 0:
        pytest.fail(f"Could not connect to Nginx at {URL}. Ensure Nginx and the Python API are running and proxying correctly.")

def test_adversarial_corpus():
    """Validate the API against the evil and clean corpora."""
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]

    assert len(evil_files) > 0, f"Evil corpus is empty in {EVIL_DIR}."
    assert len(clean_files) > 0, f"Clean corpus is empty in {CLEAN_DIR}."

    bypassed_evil = []
    for f in evil_files:
        filepath = os.path.join(EVIL_DIR, f)
        with open(filepath, 'r') as file:
            payload = json.load(file)
        status = send_request(payload)
        if status != 403:
            bypassed_evil.append(f)

    modified_clean = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_DIR, f)
        with open(filepath, 'r') as file:
            payload = json.load(file)
        status = send_request(payload)
        if status != 200:
            modified_clean.append(f)

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if errors:
        pytest.fail(" | ".join(errors))