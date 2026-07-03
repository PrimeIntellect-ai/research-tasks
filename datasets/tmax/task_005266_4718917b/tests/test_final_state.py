# test_final_state.py

import os
import json
import urllib.request
import pytest

def test_detector_compiled():
    """Verify that the C++ detector has been compiled and is executable."""
    detector_path = "/app/worker/detector"
    assert os.path.isfile(detector_path), f"{detector_path} binary does not exist. C++ program not compiled."
    assert os.access(detector_path, os.X_OK), f"{detector_path} is not executable."

def test_adversarial_corpus():
    """Verify the data filtering pipeline against the clean and evil corpora."""
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean CSV files found."
    assert len(evil_files) > 0, "No evil CSV files found."

    clean_modified = []
    evil_bypassed = []

    url = "http://localhost:5000/validate"

    # Test Clean Corpus
    for filepath in clean_files:
        data = json.dumps({"filepath": filepath}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                res = json.loads(response.read().decode('utf-8'))
                if res.get('status') != 'VALID':
                    clean_modified.append(os.path.basename(filepath))
        except Exception as e:
            clean_modified.append(os.path.basename(filepath))

    # Test Evil Corpus
    for filepath in evil_files:
        data = json.dumps({"filepath": filepath}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                res = json.loads(response.read().decode('utf-8'))
                if res.get('status') != 'ANOMALOUS':
                    evil_bypassed.append(os.path.basename(filepath))
        except Exception as e:
            evil_bypassed.append(os.path.basename(filepath))

    error_msg = ""
    if evil_bypassed:
        error_msg += f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}. "
    if clean_modified:
        error_msg += f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}."

    assert not evil_bypassed and not clean_modified, error_msg.strip()