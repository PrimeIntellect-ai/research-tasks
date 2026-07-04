# test_final_state.py

import os
import subprocess
import glob
import pytest

EXECUTABLE = "/home/user/graph_filter"
CLEAN_DIR = "/app/data/clean"
EVIL_DIR = "/app/data/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.txt"))
    assert len(clean_files) > 0, f"No files found in clean corpus directory {CLEAN_DIR}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 0 or output != "ACCEPT":
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.txt"))
    assert len(evil_files) > 0, f"No files found in evil corpus directory {EVIL_DIR}"

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 1 or output != "REJECT":
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")