# test_final_state.py
import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_vm"
CLEAN_CORPUS_PATH = "/app/configs/clean"
EVIL_CORPUS_PATH = "/app/configs/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Validation script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Validation script {SCRIPT_PATH} is not a file"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Validation script {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    if not os.path.exists(SCRIPT_PATH) or not os.access(SCRIPT_PATH, os.X_OK):
        pytest.fail(f"Script {SCRIPT_PATH} is missing or not executable.")

    clean_files = [os.path.join(CLEAN_CORPUS_PATH, f) for f in os.listdir(CLEAN_CORPUS_PATH) if f.endswith('.json')]
    evil_files = [os.path.join(EVIL_CORPUS_PATH, f) for f in os.listdir(EVIL_CORPUS_PATH) if f.endswith('.json')]

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([SCRIPT_PATH, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run([SCRIPT_PATH, ef], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))