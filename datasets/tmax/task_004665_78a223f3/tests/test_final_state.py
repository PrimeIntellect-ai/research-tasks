# test_final_state.py
import os
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/filter.sh"
CLEAN_CORPUS_DIR = "/app/data/clean/"
EVIL_CORPUS_DIR = "/app/data/evil/"

def test_filter_script_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"The script {AGENT_SCRIPT} does not exist."
    assert os.path.isfile(AGENT_SCRIPT), f"The path {AGENT_SCRIPT} is not a file."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"The script {AGENT_SCRIPT} is not executable."

def test_adversarial_corpus():
    if not os.path.exists(AGENT_SCRIPT) or not os.access(AGENT_SCRIPT, os.X_OK):
        pytest.fail("Agent script is missing or not executable; cannot run corpus tests.")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    evil_bypassed = []
    clean_rejected = []

    for evil_file in evil_files:
        result = subprocess.run([AGENT_SCRIPT, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        result = subprocess.run([AGENT_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))