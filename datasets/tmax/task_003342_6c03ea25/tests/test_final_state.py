# test_final_state.py

import os
import subprocess
import pytest

FILTER_GO = "/home/user/filter.go"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_filter_go_exists():
    assert os.path.isfile(FILTER_GO), f"File not found: {FILTER_GO}"

def test_adversarial_corpus():
    assert os.path.isfile(FILTER_GO), f"Pre-requisite failed: {FILTER_GO} does not exist"

    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS)]
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS)]

    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS}"
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS}"

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(["go", "run", FILTER_GO, f], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(["go", "run", FILTER_GO, f], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_failures[:10]))
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: " + ", ".join(clean_failures[:10]))

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))