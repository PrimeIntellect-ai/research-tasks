# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

EVIL_DIR = '/app/corpora/evil'
CLEAN_DIR = '/app/corpora/clean'
FILTER_BIN = '/home/user/filter'
URL = 'http://localhost:8080/submit'

def get_corpus_files(directory):
    if not os.path.exists(directory):
        return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def test_filter_binary_exists():
    assert os.path.exists(FILTER_BIN), f"Filter binary {FILTER_BIN} does not exist."
    assert os.access(FILTER_BIN, os.X_OK), f"Filter binary {FILTER_BIN} is not executable."

def test_filter_binary_evil_corpus():
    evil_files = get_corpus_files(EVIL_DIR)
    assert evil_files, f"No files found in {EVIL_DIR}"

    bypassed = []
    for filepath in evil_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed.append(os.path.basename(filepath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_filter_binary_clean_corpus():
    clean_files = get_corpus_files(CLEAN_DIR)
    assert clean_files, f"No files found in {CLEAN_DIR}"

    modified = []
    for filepath in clean_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            modified.append(os.path.basename(filepath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (rejected): {', '.join(modified)}")

def test_end_to_end_evil_corpus():
    evil_files = get_corpus_files(EVIL_DIR)
    assert evil_files, f"No files found in {EVIL_DIR}"

    bypassed = []
    for filepath in evil_files:
        with open(filepath, 'r') as f:
            seq = f.read().strip()
        try:
            response = requests.post(URL, data=seq, timeout=5)
            if response.status_code != 400:
                bypassed.append(os.path.basename(filepath))
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Service unreachable or crashed on {filepath}: {e}")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed via HTTP: {', '.join(bypassed)}")

def test_end_to_end_clean_corpus():
    clean_files = get_corpus_files(CLEAN_DIR)
    assert clean_files, f"No files found in {CLEAN_DIR}"

    modified = []
    for filepath in clean_files:
        with open(filepath, 'r') as f:
            seq = f.read().strip()
        try:
            response = requests.post(URL, data=seq, timeout=5)
            if response.status_code != 200:
                modified.append(os.path.basename(filepath))
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Service unreachable or crashed on {filepath}: {e}")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (rejected) via HTTP: {', '.join(modified)}")