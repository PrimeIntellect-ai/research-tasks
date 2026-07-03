# test_final_state.py

import os
import subprocess
import glob
import urllib.request
import urllib.error
import pytest

RUST_BIN = "/home/user/artifact_filter/target/release/artifact_filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
API_URL = "http://127.0.0.1:8080/api/artifacts"

def test_rust_binary_exists():
    assert os.path.isfile(RUST_BIN), f"Rust binary not found at {RUST_BIN}"
    assert os.access(RUST_BIN, os.X_OK), f"Rust binary at {RUST_BIN} is not executable"

def test_adversarial_corpus_rust_cli():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))

    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}."
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}."

    clean_failed = []
    for f in clean_files:
        res = subprocess.run([RUST_BIN, f], capture_output=True, text=True)
        if res.returncode != 0 or "ACCEPT" not in res.stdout:
            clean_failed.append(os.path.basename(f))

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run([RUST_BIN, f], capture_output=True, text=True)
        if res.returncode != 1 or "REJECT" not in res.stdout:
            evil_bypassed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)

def test_end_to_end_flow():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))

    if not clean_files or not evil_files:
        pytest.skip("Missing corpora for E2E tests.")

    # Test clean payload via API
    with open(clean_files[0], "r") as f:
        clean_data = f.read().encode("utf-8")

    req_clean = urllib.request.Request(API_URL, data=clean_data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req_clean) as response:
            assert response.status == 200, f"Expected 200 OK for clean payload, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Clean payload failed with status {e.code}")
    except Exception as e:
        pytest.fail(f"Could not connect to API for clean payload E2E test: {e}")

    # Test evil payload via API
    with open(evil_files[0], "r") as f:
        evil_data = f.read().encode("utf-8")

    req_evil = urllib.request.Request(API_URL, data=evil_data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req_evil) as response:
            pytest.fail(f"Expected 406 Not Acceptable for evil payload, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 406, f"Expected 406 Not Acceptable for evil payload, got {e.code}"
    except Exception as e:
        pytest.fail(f"Could not connect to API for evil payload E2E test: {e}")