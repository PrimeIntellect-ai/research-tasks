# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitizer.sh"
CLEAN_CORPUS = "/verify/corpus/clean"
EVIL_CORPUS = "/verify/corpus/evil"

def test_sanitizer_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_clean_corpus():
    if not os.path.exists(CLEAN_CORPUS):
        pytest.skip("Clean corpus not found")

    failed_files = []
    for filename in sorted(os.listdir(CLEAN_CORPUS)):
        filepath = os.path.join(CLEAN_CORPUS, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, 'rb') as f:
            expected_content = f.read()

        result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)

        if result.returncode != 0 or result.stdout != expected_content:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} clean files modified or rejected: {failed_files}"

def test_evil_corpus():
    if not os.path.exists(EVIL_CORPUS):
        pytest.skip("Evil corpus not found")

    failed_files = []
    for filename in sorted(os.listdir(EVIL_CORPUS)):
        filepath = os.path.join(EVIL_CORPUS, filename)
        if not os.path.isfile(filepath):
            continue

        result = subprocess.run(["bash", SCRIPT_PATH, filepath], capture_output=True)

        if result.returncode != 1 or result.stdout != b"":
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} evil files bypassed: {failed_files}"