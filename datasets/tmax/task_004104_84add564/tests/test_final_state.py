# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_schema.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists_and_executable():
    """Verify the validation script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_adversarial_corpus_validation():
    """Test the solution against the clean and evil corpora."""
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    clean_failures = []
    for filepath in clean_files:
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(filepath))

    evil_failures = []
    for filepath in evil_files:
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(filepath))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))