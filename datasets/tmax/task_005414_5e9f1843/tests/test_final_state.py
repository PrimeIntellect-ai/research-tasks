# test_final_state.py

import os
import glob
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/jwt_analyzer.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_jwt_analyzer_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"The script {AGENT_SCRIPT} does not exist."

def test_adversarial_corpus_evaluation():
    assert os.path.isfile(AGENT_SCRIPT), f"The script {AGENT_SCRIPT} does not exist."

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.txt"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.txt"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failures = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", AGENT_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(clean_file))

    evil_failures = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", AGENT_SCRIPT, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(evil_file))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures[:10])}{'...' if len(evil_failures) > 10 else ''}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures[:10])}{'...' if len(clean_failures) > 10 else ''}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))