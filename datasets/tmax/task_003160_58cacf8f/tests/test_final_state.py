# test_final_state.py

import os
import glob
import json
import subprocess
import urllib.request
import urllib.error
import pytest

DETECTOR_PATH = "/home/user/detector.py"
CLEAN_CORPUS_PATHS = ["/home/user/corpora/clean", "/opt/verifier/corpora/clean"]
EVIL_CORPUS_PATHS = ["/home/user/corpora/evil", "/opt/verifier/corpora/evil"]
INGEST_URL = "http://localhost:8080/ingest"

def get_files_from_paths(paths):
    files = []
    for path in paths:
        if os.path.isdir(path):
            files.extend(glob.glob(os.path.join(path, "*")))
    return files

def test_detector_exists():
    assert os.path.isfile(DETECTOR_PATH), f"Detector script not found at {DETECTOR_PATH}"

def test_detector_clean_corpus():
    clean_files = get_files_from_paths(CLEAN_CORPUS_PATHS)
    assert clean_files, "No clean corpus files found."

    failed_files = []
    for file_path in clean_files:
        result = subprocess.run(["python3", DETECTOR_PATH, file_path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}")

def test_detector_evil_corpus():
    evil_files = get_files_from_paths(EVIL_CORPUS_PATHS)
    assert evil_files, "No evil corpus files found."

    failed_files = []
    for file_path in evil_files:
        result = subprocess.run(["python3", DETECTOR_PATH, file_path], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}")

def test_end_to_end_clean():
    clean_files = get_files_from_paths(CLEAN_CORPUS_PATHS)
    assert clean_files, "No clean corpus files found."

    failed_files = []
    for file_path in clean_files:
        with open(file_path, "rb") as f:
            data = f.read()

        req = urllib.request.Request(INGEST_URL, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    failed_files.append(os.path.basename(file_path))
        except urllib.error.HTTPError as e:
            failed_files.append(f"{os.path.basename(file_path)} (HTTP {e.code})")
        except Exception as e:
            failed_files.append(f"{os.path.basename(file_path)} (Error: {e})")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean payloads failed end-to-end: {', '.join(failed_files)}")

def test_end_to_end_evil():
    evil_files = get_files_from_paths(EVIL_CORPUS_PATHS)
    assert evil_files, "No evil corpus files found."

    failed_files = []
    for file_path in evil_files:
        with open(file_path, "rb") as f:
            data = f.read()

        req = urllib.request.Request(INGEST_URL, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                # If it succeeds, it bypassed the filter
                failed_files.append(os.path.basename(file_path))
        except urllib.error.HTTPError as e:
            if e.code != 400:
                failed_files.append(f"{os.path.basename(file_path)} (Expected 400, got {e.code})")
        except Exception as e:
            failed_files.append(f"{os.path.basename(file_path)} (Error: {e})")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil payloads bypassed end-to-end: {', '.join(failed_files)}")