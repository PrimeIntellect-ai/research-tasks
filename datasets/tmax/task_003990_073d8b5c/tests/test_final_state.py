# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_sanitizer_exists_and_executable():
    """Test that the compiled C program exists and is executable."""
    sanitizer_path = "/home/user/loc_sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer executable is missing: {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer is not executable: {sanitizer_path}"

def test_adversarial_corpus():
    """Test the sanitizer against the clean and evil corpora."""
    sanitizer_path = "/home/user/loc_sanitizer"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isfile(sanitizer_path), "Sanitizer executable not found."

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    failed_clean = []
    for f in clean_files:
        result = subprocess.run([sanitizer_path, f], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        result = subprocess.run([sanitizer_path, f], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(f))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean files modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed: {', '.join(failed_evil)}")

    assert not errors, " | ".join(errors)