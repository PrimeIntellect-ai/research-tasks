# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/ci_guard.sh"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"The script {SCRIPT_PATH} is not executable."

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus missing at {CLEAN_CORPUS}"
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus missing at {EVIL_CORPUS}"

    clean_projects = sorted([os.path.join(CLEAN_CORPUS, d) for d in os.listdir(CLEAN_CORPUS) if os.path.isdir(os.path.join(CLEAN_CORPUS, d))])
    evil_projects = sorted([os.path.join(EVIL_CORPUS, d) for d in os.listdir(EVIL_CORPUS) if os.path.isdir(os.path.join(EVIL_CORPUS, d))])

    assert len(clean_projects) > 0, "No clean projects found."
    assert len(evil_projects) > 0, "No evil projects found."

    clean_failures = []
    for proj in clean_projects:
        result = subprocess.run([SCRIPT_PATH, proj], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(proj))

    evil_failures = []
    for proj in evil_projects:
        result = subprocess.run([SCRIPT_PATH, proj], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(proj))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_projects)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_projects)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))