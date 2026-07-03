# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def send_request(sequence):
    url = "http://127.0.0.1:8080/analyze"
    data = json.dumps({"sequence": sequence}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_body = response.read().decode('utf-8')
            return json.loads(res_body).get("status")
    except Exception as e:
        return f"Error: {str(e)}"

def test_adversarial_corpus():
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory not found at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory not found at {clean_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus"
    assert len(clean_files) > 0, "No files found in clean corpus"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, 'r') as f:
            sequence = f.read().strip()
        status = send_request(sequence)
        if status != "evil":
            evil_bypassed.append(filename)

    # Test clean corpus
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, 'r') as f:
            sequence = f.read().strip()
        status = send_request(sequence)
        if status != "clean":
            clean_modified.append(filename)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified. Offending files: {', '.join(clean_modified)}")

    if error_msg:
        pytest.fail("\n".join(error_msg))