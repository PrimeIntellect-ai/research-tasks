# test_final_state.py

import os
import subprocess
import tempfile
import hashlib
import pytest
import requests

EVIL_DIR = "/home/user/corpora/evil/"
CLEAN_DIR = "/home/user/corpora/clean/"
FILTER_SCRIPT = "/home/user/app/artifact_filter.py"
GATEWAY_URL = "http://127.0.0.1:5000/upload"
STORAGE_DIR = "/home/user/app/storage/"

def test_artifact_filter_evil_corpus():
    assert os.path.isfile(FILTER_SCRIPT), f"Missing filter script: {FILTER_SCRIPT}"
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus"

    bypassed = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for fname in evil_files:
            fpath = os.path.join(EVIL_DIR, fname)
            result = subprocess.run(["python3", FILTER_SCRIPT, fpath, tmpdir], capture_output=True)
            if result.returncode == 0:
                bypassed.append(fname)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_artifact_filter_clean_corpus():
    assert os.path.isfile(FILTER_SCRIPT), f"Missing filter script: {FILTER_SCRIPT}"
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus"

    modified = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for fname in clean_files:
            fpath = os.path.join(CLEAN_DIR, fname)

            with open(fpath, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            expected_out = os.path.join(tmpdir, f"{file_hash}.czip")

            result = subprocess.run(["python3", FILTER_SCRIPT, fpath, tmpdir], capture_output=True)
            if result.returncode != 0 or not os.path.isfile(expected_out):
                modified.append(fname)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (or rejected): {', '.join(modified)}")

def test_gateway_upload_clean():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    failed = []

    for fname in clean_files:
        fpath = os.path.join(CLEAN_DIR, fname)
        with open(fpath, 'rb') as f:
            file_data = f.read()
            file_hash = hashlib.sha256(file_data).hexdigest()

        try:
            resp = requests.post(GATEWAY_URL, files={'file': (fname, file_data)}, timeout=5)
            if resp.status_code != 200:
                failed.append(fname)
            else:
                expected_storage = os.path.join(STORAGE_DIR, f"{file_hash}.czip")
                if not os.path.isfile(expected_storage):
                    failed.append(fname + " (not in storage)")
        except Exception as e:
            failed.append(fname + f" (error: {e})")

    if failed:
        pytest.fail(f"Gateway failed to process clean files: {', '.join(failed)}")

def test_gateway_upload_evil():
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    bypassed = []

    for fname in evil_files:
        fpath = os.path.join(EVIL_DIR, fname)
        with open(fpath, 'rb') as f:
            file_data = f.read()
            file_hash = hashlib.sha256(file_data).hexdigest()

        try:
            resp = requests.post(GATEWAY_URL, files={'file': (fname, file_data)}, timeout=5)
            if resp.status_code == 200:
                bypassed.append(fname)
            else:
                expected_storage = os.path.join(STORAGE_DIR, f"{file_hash}.czip")
                if os.path.isfile(expected_storage):
                    bypassed.append(fname + " (found in storage despite error)")
        except Exception:
            pass # Expected to possibly fail or return 400/500

    if bypassed:
        pytest.fail(f"Gateway bypassed evil files: {', '.join(bypassed)}")