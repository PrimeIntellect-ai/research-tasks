# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest
import time

FILTER_BIN = "/home/user/filter"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"
UPLOAD_URL = "http://localhost:8080/upload"

def test_filter_executable_corpus():
    """
    Adversarial corpus test:
    Iterates over evil and clean corpora, asserting the filter rejects evil and accepts clean.
    """
    assert os.path.isfile(FILTER_BIN), f"Filter binary not found at {FILTER_BIN}"
    assert os.access(FILTER_BIN, os.X_OK), f"Filter binary is not executable at {FILTER_BIN}"

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        res = subprocess.run([FILTER_BIN, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        res = subprocess.run([FILTER_BIN, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    err_msgs = []
    if evil_failed:
        err_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        err_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    if err_msgs:
        pytest.fail(" | ".join(err_msgs))

def test_server_integration():
    """
    Tests the end-to-end integration by sending a clean and an evil file to the Tracker Service.
    """
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    if not clean_files or not evil_files:
        pytest.skip("Corpus files missing, cannot test server integration.")

    # Wait for the server to be available if it was just started
    server_up = False
    for _ in range(5):
        try:
            req = urllib.request.Request(UPLOAD_URL, method="OPTIONS")
            urllib.request.urlopen(req, timeout=1)
            server_up = True
            break
        except Exception:
            time.sleep(1)

    if not server_up:
        # We will still attempt the POSTs below, which will fail with a clear connection error if the server is down
        pass

    # Test Clean Upload
    clean_sample = clean_files[0]
    with open(clean_sample, "rb") as f:
        clean_data = f.read()

    req_clean = urllib.request.Request(UPLOAD_URL, data=clean_data, method="POST")
    try:
        with urllib.request.urlopen(req_clean, timeout=5) as response:
            assert response.status == 200, f"Clean file upload expected HTTP 200, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Clean file upload failed with HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Tracker Service at {UPLOAD_URL}: {e.reason}")

    # Test Evil Upload
    evil_sample = evil_files[0]
    with open(evil_sample, "rb") as f:
        evil_data = f.read()

    req_evil = urllib.request.Request(UPLOAD_URL, data=evil_data, method="POST")
    try:
        with urllib.request.urlopen(req_evil, timeout=5) as response:
            pytest.fail(f"Evil file upload expected HTTP 403, but succeeded with HTTP {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Evil file upload expected HTTP 403, got HTTP {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Tracker Service at {UPLOAD_URL}: {e.reason}")