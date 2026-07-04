# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_config.sh"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert clean_files, "No files found in clean corpus directory"

    modified_files = []
    for f in clean_files:
        config_path = os.path.join(CLEAN_CORPUS, f)
        result = subprocess.run([SCRIPT_PATH, config_path], capture_output=True, text=True)
        if result.returncode != 0:
            modified_files.append(f)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean configs modified/rejected (expected exit code 0). Offending files: {', '.join(modified_files)}")

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert evil_files, "No files found in evil corpus directory"

    bypassed_files = []
    for f in evil_files:
        config_path = os.path.join(EVIL_CORPUS, f)
        result = subprocess.run([SCRIPT_PATH, config_path], capture_output=True, text=True)
        if result.returncode != 1:
            bypassed_files.append(f)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil configs bypassed (expected exit code 1). Offending files: {', '.join(bypassed_files)}")