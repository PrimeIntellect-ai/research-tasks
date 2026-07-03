# test_final_state.py
import os
import glob
import subprocess
import time
import urllib.request
import urllib.error
import pytest

CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
VALIDATOR_SCRIPT = "/home/user/validator.py"
START_SCRIPT = "/home/user/start_pipeline.sh"

def test_validator_script_exists():
    assert os.path.isfile(VALIDATOR_SCRIPT), f"Validator script {VALIDATOR_SCRIPT} does not exist."

def test_start_script_exists_and_executable():
    assert os.path.isfile(START_SCRIPT), f"Start script {START_SCRIPT} does not exist."
    assert os.access(START_SCRIPT, os.X_OK), f"Start script {START_SCRIPT} is not executable."

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for f in clean_files:
        res = subprocess.run(["python3", VALIDATOR_SCRIPT, f], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        res = subprocess.run(["python3", VALIDATOR_SCRIPT, f], capture_output=True)
        if res.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean files rejected: {', '.join(clean_failures[:5])}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil files bypassed: {', '.join(evil_failures[:5])}")

    assert not error_msg, " | ".join(error_msg)

def test_end_to_end_pipeline():
    # Execute the start pipeline script
    subprocess.run([START_SCRIPT], shell=True, check=True)
    time.sleep(2)

    # Test with a clean file
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    assert len(clean_files) > 0, "No clean files found for e2e test."
    clean_file = clean_files[0]

    with open(clean_file, 'rb') as f:
        data = f.read()

    req = urllib.request.Request("http://127.0.0.1:8080/upload", data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200 for clean file, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP request failed for clean file: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"Connection failed: {e.reason}. Is Nginx and Flask running on port 8080?")

    # Test with an evil file
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))
    assert len(evil_files) > 0, "No evil files found for e2e test."
    evil_file = evil_files[0]

    with open(evil_file, 'rb') as f:
        data = f.read()

    req = urllib.request.Request("http://127.0.0.1:8080/upload", data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            pytest.fail(f"Expected HTTP 400 for evil file, got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400 for evil file, got {e.code}"