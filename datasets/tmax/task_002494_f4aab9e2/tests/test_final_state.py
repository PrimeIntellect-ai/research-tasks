# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE = "/home/user/stream_filter"
EVIL_DIR = "/app/corpus/evil/"
CLEAN_DIR = "/app/corpus/clean/"

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} not found. Did you compile your C program?"
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_adversarial_corpus():
    """Test the stream filter against the evil and clean corpora."""

    # Ensure directories exist
    assert os.path.isdir(EVIL_DIR), f"Evil directory {EVIL_DIR} missing."
    assert os.path.isdir(CLEAN_DIR), f"Clean directory {CLEAN_DIR} missing."

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    bypassed_evil = []
    modified_clean = []

    # Test Evil Corpus
    for ef in evil_files:
        with open(ef, 'rb') as f:
            result = subprocess.run([EXECUTABLE], stdin=f, capture_output=True)
            # Evil files must be rejected with exit code 1
            if result.returncode != 1:
                bypassed_evil.append(os.path.basename(ef))

    # Test Clean Corpus
    for cf in clean_files:
        with open(cf, 'rb') as f:
            original_data = f.read()
            f.seek(0)
            result = subprocess.run([EXECUTABLE], stdin=f, capture_output=True)
            # Clean files must be accepted (exit code 0) and stdout must match input exactly
            if result.returncode != 0 or result.stdout != original_data:
                modified_clean.append(os.path.basename(cf))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))