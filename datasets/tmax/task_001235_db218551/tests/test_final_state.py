# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_manifest.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_script_exists():
    """Test that the validation script exists."""
    assert os.path.isfile(SCRIPT_PATH), f"Validation script missing at {SCRIPT_PATH}"

def test_adversarial_corpus():
    """Test the validation script against the clean and evil corpora."""
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus missing at {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus missing at {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "Clean corpus is empty"
    assert len(evil_files) > 0, "Evil corpus is empty"

    failed_clean = []
    failed_evil = []

    # Test clean corpus
    for clean_file in clean_files:
        result = subprocess.run(["bash", SCRIPT_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(clean_file))

    # Test evil corpus
    for evil_file in evil_files:
        result = subprocess.run(["bash", SCRIPT_PATH, evil_file], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(evil_file))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))