# test_final_state.py

import os
import stat
import subprocess
import pytest

EXECUTABLE_PATH = "/home/user/sequence_filter"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_executable_exists_and_is_executable():
    assert os.path.isfile(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}"
    st = os.stat(EXECUTABLE_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"File at {EXECUTABLE_PATH} is not executable"

def test_adversarial_corpus():
    # Ensure executable is present
    if not os.path.isfile(EXECUTABLE_PATH):
        pytest.fail(f"Executable not found at {EXECUTABLE_PATH}")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".fasta")]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".fasta")]

    assert len(evil_files) > 0, f"No evil fasta files found in {EVIL_CORPUS_DIR}"
    assert len(clean_files) > 0, f"No clean fasta files found in {CLEAN_CORPUS_DIR}"

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        result = subprocess.run([EXECUTABLE_PATH, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        result = subprocess.run([EXECUTABLE_PATH, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))