# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter.sh"
EVIL_DIR = "/app/verifier/evil"
CLEAN_DIR = "/app/verifier/clean"
METADATA_CSV = "/app/verifier/metadata.csv"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"

    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.txt')]
    assert len(evil_files) > 0, f"No text files found in evil corpus: {EVIL_DIR}"

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        result = subprocess.run([SCRIPT_PATH, filepath, METADATA_CSV], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the filter (expected exit code 1). Offending files: {', '.join(bypassed_files)}")

def test_clean_corpus_accepted():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.txt')]
    assert len(clean_files) > 0, f"No text files found in clean corpus: {CLEAN_DIR}"

    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        result = subprocess.run([SCRIPT_PATH, filepath, METADATA_CSV], capture_output=True)
        if result.returncode != 0:
            modified_files.append((filename, result.returncode))

    if modified_files:
        offending_names = [f[0] for f in modified_files]
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean files were rejected or errored (expected exit code 0). Offending files: {', '.join(offending_names)}")