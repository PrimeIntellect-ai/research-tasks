# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/check_py3_ready.sh"
EVIL_CORPUS_DIR = "/app/corpora/evil/"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_adversarial_corpus():
    # Ensure corpora directories exist
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} missing."
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} missing."

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.py')]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.py')]

    assert len(evil_files) > 0, "No python files found in evil corpus."
    assert len(clean_files) > 0, "No python files found in clean corpus."

    evil_bypassed = []
    clean_rejected = []

    # Test evil corpus
    for evil_file in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, evil_file)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(evil_file)

    # Test clean corpus
    for clean_file in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, clean_file)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(clean_file)

    error_messages = []
    if evil_bypassed:
        error_messages.append(
            f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}"
        )
    if clean_rejected:
        error_messages.append(
            f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}"
        )

    if error_messages:
        pytest.fail(" | ".join(error_messages))