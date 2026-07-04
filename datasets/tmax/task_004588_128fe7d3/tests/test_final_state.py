# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/paper_filter.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Target script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_adversarial_corpus():
    assert os.path.exists(SCRIPT_PATH), f"Target script {SCRIPT_PATH} does not exist."

    clean_files = os.listdir(CLEAN_CORPUS_DIR) if os.path.exists(CLEAN_CORPUS_DIR) else []
    evil_files = os.listdir(EVIL_CORPUS_DIR) if os.path.exists(EVIL_CORPUS_DIR) else []

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_failures = []
    for paper_id in clean_files:
        result = subprocess.run(
            ["python", SCRIPT_PATH, paper_id],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            clean_failures.append(paper_id)

    evil_failures = []
    for paper_id in evil_files:
        result = subprocess.run(
            ["python", SCRIPT_PATH, paper_id],
            capture_output=True,
            text=True
        )
        if result.returncode != 1:
            evil_failures.append(paper_id)

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures[:5])}{'...' if len(clean_failures) > 5 else ''}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_failures[:5])}{'...' if len(evil_failures) > 5 else ''}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))