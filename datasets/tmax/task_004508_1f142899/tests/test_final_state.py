# test_final_state.py

import os
import glob
import urllib.request
import urllib.error
import pytest

def send_request(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    req = urllib.request.Request("http://127.0.0.1:8080/ingest", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return None

def test_detector_script_exists():
    assert os.path.isfile("/home/user/detector.py"), "The script /home/user/detector.py is missing."

def test_clean_corpus():
    clean_files = glob.glob("/app/data/clean/*.json")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_clean = []
    for filepath in clean_files:
        status = send_request(filepath)
        if status != 200:
            failed_clean.append((os.path.basename(filepath), status))

    if failed_clean:
        details = ", ".join([f"{name} (HTTP {status})" for name, status in failed_clean])
        pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean files were modified/rejected or failed to process: {details}")

def test_evil_corpus():
    evil_files = glob.glob("/app/data/evil/*.json")
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_evil = []
    for filepath in evil_files:
        status = send_request(filepath)
        if status != 406:
            failed_evil.append((os.path.basename(filepath), status))

    if failed_evil:
        details = ", ".join([f"{name} (HTTP {status})" for name, status in failed_evil])
        pytest.fail(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed detection or failed to process: {details}")