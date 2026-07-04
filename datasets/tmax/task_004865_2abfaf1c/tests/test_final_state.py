# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE_PATH = "/home/user/dataset_filter/target/release/dataset_filter"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.exists(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}"
    assert os.path.isfile(EXECUTABLE_PATH), f"Path is not a file: {EXECUTABLE_PATH}"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File is not executable: {EXECUTABLE_PATH}"

def test_clean_corpus():
    if not os.path.exists(EXECUTABLE_PATH):
        pytest.skip("Executable not found")

    clean_dirs = [os.path.join(CLEAN_CORPUS, d) for d in os.listdir(CLEAN_CORPUS) if os.path.isdir(os.path.join(CLEAN_CORPUS, d))]
    assert len(clean_dirs) > 0, f"No clean directories found in {CLEAN_CORPUS}"

    failed_clean = []
    for clean_dir in clean_dirs:
        result = subprocess.run([EXECUTABLE_PATH, clean_dir], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(clean_dir))

    if failed_clean:
        pytest.fail(f"{len(failed_clean)} of {len(clean_dirs)} clean directories modified/rejected. Offending: {', '.join(failed_clean)}")

def test_evil_corpus():
    if not os.path.exists(EXECUTABLE_PATH):
        pytest.skip("Executable not found")

    evil_dirs = [os.path.join(EVIL_CORPUS, d) for d in os.listdir(EVIL_CORPUS) if os.path.isdir(os.path.join(EVIL_CORPUS, d))]
    assert len(evil_dirs) > 0, f"No evil directories found in {EVIL_CORPUS}"

    failed_evil = []
    for evil_dir in evil_dirs:
        result = subprocess.run([EXECUTABLE_PATH, evil_dir], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(evil_dir))

    if failed_evil:
        pytest.fail(f"{len(failed_evil)} of {len(evil_dirs)} evil directories bypassed. Offending: {', '.join(failed_evil)}")