# test_final_state.py

import os
import subprocess
import pytest

EVIL_DIR = "/app/corpus/evil"
CLEAN_DIR = "/app/corpus/clean"
SANITIZER_PATH = "/home/user/sanitizer"
COUNT_FILE = "/home/user/clean_frame_count.txt"

def test_sanitizer_exists_and_executable():
    """Ensure the sanitizer binary exists and is executable."""
    assert os.path.isfile(SANITIZER_PATH), f"Sanitizer not found at {SANITIZER_PATH}"
    assert os.access(SANITIZER_PATH, os.X_OK), f"Sanitizer at {SANITIZER_PATH} is not executable"

def test_sanitizer_on_corpus():
    """Test the sanitizer against the adversarial corpus."""
    if not os.path.isfile(SANITIZER_PATH):
        pytest.fail(f"Sanitizer not found at {SANITIZER_PATH}")

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_DIR}"
    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_DIR}"

    evil_bypassed = []
    clean_modified = []

    for e_file in evil_files:
        result = subprocess.run([SANITIZER_PATH, e_file], capture_output=True)
        # Exit code 1 means rejected (evil), 0 means accepted (clean)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(e_file))

    for c_file in clean_files:
        result = subprocess.run([SANITIZER_PATH, c_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(c_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:10])}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified[:10])}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_clean_frame_count():
    """Ensure the clean frame count file contains the expected value."""
    assert os.path.isfile(COUNT_FILE), f"Count file not found at {COUNT_FILE}"
    with open(COUNT_FILE, "r") as f:
        content = f.read().strip()

    try:
        count = int(content)
    except ValueError:
        pytest.fail(f"Content of {COUNT_FILE} is not a valid integer: '{content}'")

    assert count == 45, f"Expected 45 clean frames, but found {count}"