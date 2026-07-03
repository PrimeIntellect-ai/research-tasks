# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE = "/home/user/sanitizer"
EVIL_DIR = "/app/corpus/evil"
CLEAN_DIR = "/app/corpus/clean"

def test_sanitizer_exists_and_executable():
    assert os.path.exists(EXECUTABLE), f"Sanitizer executable not found at {EXECUTABLE}"
    assert os.path.isfile(EXECUTABLE), f"Sanitizer path {EXECUTABLE} is not a file"
    assert os.access(EXECUTABLE, os.X_OK), f"Sanitizer executable at {EXECUTABLE} is not executable"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    # Test Evil Corpus
    for filepath in evil_files:
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)
        # Pass criterion for evil: exit code 1 AND stdout contains EVIL
        if result.returncode != 1 or "EVIL" not in result.stdout:
            evil_bypassed.append(os.path.basename(filepath))

    # Test Clean Corpus
    for filepath in clean_files:
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)
        # Pass criterion for clean: exit code 0 AND stdout contains CLEAN
        if result.returncode != 0 or "CLEAN" not in result.stdout:
            clean_modified.append(os.path.basename(filepath))

    total_evil = len(evil_files)
    total_clean = len(clean_files)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {total_evil} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {total_clean} clean modified (rejected): {', '.join(clean_modified)}")

    if errors:
        pytest.fail("Adversarial corpus validation failed. " + " | ".join(errors))