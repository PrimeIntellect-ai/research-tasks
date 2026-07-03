# test_final_state.py

import os
import subprocess
import json
import urllib.request
import urllib.error
import pytest

CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
FILTER_BIN = "/home/user/spectro_filter"

def run_filter(filepath):
    """Run the Go binary on the given filepath and return the exit code."""
    result = subprocess.run(
        [FILTER_BIN, filepath],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode

def test_go_binary_adversarial_corpus():
    """Test the Go binary directly against the clean and evil corpora."""
    assert os.path.isfile(FILTER_BIN), f"Go binary not found at {FILTER_BIN}"
    assert os.access(FILTER_BIN, os.X_OK), f"Go binary at {FILTER_BIN} is not executable"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_modified = []
    for cf in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, cf)
        if run_filter(filepath) != 0:
            clean_modified.append(cf)

    evil_bypassed = []
    for ef in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, ef)
        if run_filter(filepath) != 1:
            evil_bypassed.append(ef)

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_multi_service_composition():
    """Test the end-to-end ingestion pipeline via the Python API and Redis."""
    # Ensure Redis is running and clear the list first
    try:
        subprocess.run(["redis-cli", "DEL", "valid_spectra"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to connect to Redis or execute DEL command. Is Redis running?")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]

    # Send clean files
    for cf in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, cf)
        with open(filepath, 'rb') as f:
            data = f.read()
        req = urllib.request.Request("http://127.0.0.1:8000/ingest", data=data, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to send request to ingestion API: {e}")

    # Send evil files
    for ef in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, ef)
        with open(filepath, 'rb') as f:
            data = f.read()
        req = urllib.request.Request("http://127.0.0.1:8000/ingest", data=data, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to send request to ingestion API: {e}")

    # Check Redis list length
    result = subprocess.run(["redis-cli", "LLEN", "valid_spectra"], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail("Failed to query Redis for valid_spectra length.")

    try:
        llen = int(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Unexpected output from Redis LLEN: {result.stdout}")

    assert llen == len(clean_files), f"Expected {len(clean_files)} items in Redis list 'valid_spectra', but found {llen}."