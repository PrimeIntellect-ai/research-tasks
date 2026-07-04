# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import pytest

CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"
CLASSIFICATION_FILE = "/home/user/classification.json"

def test_classification_json():
    assert os.path.isfile(CLASSIFICATION_FILE), f"Classification file missing: {CLASSIFICATION_FILE}"

    with open(CLASSIFICATION_FILE, "r") as f:
        try:
            classification = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {CLASSIFICATION_FILE}")

    clean_files = os.listdir(CLEAN_DIR)
    evil_files = os.listdir(EVIL_DIR)

    evil_bypassed = []
    clean_modified = []

    for c_file in clean_files:
        if classification.get(c_file) != "clean":
            clean_modified.append(c_file)

    for e_file in evil_files:
        if classification.get(e_file) != "evil":
            evil_bypassed.append(e_file)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (not classified 'clean'): {', '.join(clean_modified)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))

def post_request(url, data):
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

def test_waf_direct_http():
    clean_files = os.listdir(CLEAN_DIR)
    evil_files = os.listdir(EVIL_DIR)

    evil_bypassed = []
    clean_modified = []

    for c_file in clean_files:
        with open(os.path.join(CLEAN_DIR, c_file), "rb") as f:
            data = f.read()
        status, _ = post_request("http://localhost:5000/", data)
        if status != 200:
            clean_modified.append(c_file)

    for e_file in evil_files:
        with open(os.path.join(EVIL_DIR, e_file), "rb") as f:
            data = f.read()
        status, _ = post_request("http://localhost:5000/", data)
        if status != 403:
            evil_bypassed.append(e_file)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed WAF directly: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected by WAF directly): {', '.join(clean_modified)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))

def test_end_to_end_proxy():
    clean_files = os.listdir(CLEAN_DIR)
    evil_files = os.listdir(EVIL_DIR)

    if not clean_files or not evil_files:
        pytest.fail("Corpus directories are empty.")

    # Test clean payload via proxy
    c_file = clean_files[0]
    with open(os.path.join(CLEAN_DIR, c_file), "rb") as f:
        clean_data = f.read()

    status, body = post_request("http://localhost:8000/", clean_data)
    assert status == 200, f"Expected 200 OK from Proxy for clean payload, got {status}"

    try:
        resp_json = json.loads(body)
        assert resp_json.get("status") == "success" and resp_json.get("data") == "processed", \
            f"Expected backend response {{'status': 'success', 'data': 'processed'}}, got {resp_json}"
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response from proxy/backend, got: {body}")

    # Test evil payload via proxy
    e_file = evil_files[0]
    with open(os.path.join(EVIL_DIR, e_file), "rb") as f:
        evil_data = f.read()

    status, _ = post_request("http://localhost:8000/", evil_data)
    assert status == 403, f"Expected 403 Forbidden from Proxy for evil payload, got {status}"