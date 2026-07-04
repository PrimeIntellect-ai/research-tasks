# test_final_state.py

import os
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/filter.sh"
EVIL_CORPUS = "/app/corpora/evil"
CLEAN_CORPUS = "/app/corpora/clean"

def test_filter_script_exists_and_executable():
    assert os.path.isfile(FILTER_SCRIPT), f"Filter script {FILTER_SCRIPT} is missing."
    assert os.access(FILTER_SCRIPT, os.X_OK), f"Filter script {FILTER_SCRIPT} is not executable."

def test_filter_rejects_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert len(evil_files) > 0, "Evil corpus is empty."

    bypassed = []
    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS, f)
        with open(filepath, 'r') as fp:
            payload = fp.read()

        result = subprocess.run(["bash", FILTER_SCRIPT], input=payload.encode('utf-8'), capture_output=True)
        if result.returncode == 0:
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed[:5]}")

def test_filter_accepts_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "Clean corpus is empty."

    modified = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS, f)
        with open(filepath, 'r') as fp:
            payload = fp.read()

        result = subprocess.run(["bash", FILTER_SCRIPT], input=payload.encode('utf-8'), capture_output=True)
        if result.returncode != 0:
            modified.append(f)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (rejected): {modified[:5]}")