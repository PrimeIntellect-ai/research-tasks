# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE = "/home/user/sanitizer"
CLEAN_DIR = "/app/corpus/clean/"
EVIL_DIR = "/app/corpus/evil/"

def test_executable_exists():
    assert os.path.exists(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.path.isfile(EXECUTABLE), f"{EXECUTABLE} is not a file"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not marked as executable"

def test_clean_corpus_accepted():
    if not os.path.exists(EXECUTABLE):
        pytest.skip("Executable missing, cannot run corpus tests.")

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, f"No files found in clean corpus directory: {CLEAN_DIR}"

    failed_files = []
    for fpath in clean_files:
        with open(fpath, "rb") as f:
            result = subprocess.run([EXECUTABLE], stdin=f, capture_output=True)
            if result.returncode != 0:
                failed_files.append((os.path.basename(fpath), result.returncode))

    if failed_files:
        details = ", ".join([f"{name} (code {code})" for name, code in failed_files[:5]])
        if len(failed_files) > 5:
            details += f" ... and {len(failed_files) - 5} more"
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected. Examples: {details}")

def test_evil_corpus_rejected():
    if not os.path.exists(EXECUTABLE):
        pytest.skip("Executable missing, cannot run corpus tests.")

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, f"No files found in evil corpus directory: {EVIL_DIR}"

    failed_files = []
    for fpath in evil_files:
        with open(fpath, "rb") as f:
            result = subprocess.run([EXECUTABLE], stdin=f, capture_output=True)
            if result.returncode == 0:
                failed_files.append(os.path.basename(fpath))

    if failed_files:
        details = ", ".join(failed_files[:5])
        if len(failed_files) > 5:
            details += f" ... and {len(failed_files) - 5} more"
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed the sanitizer (exited with 0). Examples: {details}")