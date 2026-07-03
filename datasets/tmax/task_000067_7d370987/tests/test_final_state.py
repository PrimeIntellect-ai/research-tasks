# test_final_state.py
import os
import subprocess
import pytest

EVIL_CORPUS_PATH = "/app/corpus/evil/"
CLEAN_CORPUS_PATH = "/app/corpus/clean/"
SCRIPT_PATH = "/home/user/sanitizer.py"

def test_sanitizer_exists():
    """Test that the sanitizer script was created."""
    assert os.path.isfile(SCRIPT_PATH), f"Sanitizer script missing at {SCRIPT_PATH}"

def test_sanitizer_adversarial_corpus():
    """Test that the sanitizer correctly classifies clean and evil files."""
    assert os.path.isfile(SCRIPT_PATH), f"Sanitizer script missing at {SCRIPT_PATH}"

    evil_files = [os.path.join(EVIL_CORPUS_PATH, f) for f in os.listdir(EVIL_CORPUS_PATH) if f.endswith('.wav')]
    clean_files = [os.path.join(CLEAN_CORPUS_PATH, f) for f in os.listdir(CLEAN_CORPUS_PATH) if f.endswith('.wav')]

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        result = subprocess.run(["python", SCRIPT_PATH, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        result = subprocess.run(["python", SCRIPT_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))