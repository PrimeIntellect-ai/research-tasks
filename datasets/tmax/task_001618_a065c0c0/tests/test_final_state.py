# test_final_state.py
import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/sanitizer.sh"

def test_sanitizer_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_sanitizer_clean_corpus():
    clean_dir = "/app/corpus/clean"
    clean_files = [f for f in glob.glob(os.path.join(clean_dir, "*")) if os.path.isfile(f)]
    assert len(clean_files) > 0, f"No clean files found in {clean_dir}."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        # Clean files must exit with 0 (preserve)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected incorrectly (expected exit code 0). Offending files: {', '.join(failed_files)}")

def test_sanitizer_evil_corpus():
    evil_dir = "/app/corpus/evil"
    evil_files = [f for f in glob.glob(os.path.join(evil_dir, "*")) if os.path.isfile(f)]
    assert len(evil_files) > 0, f"No evil files found in {evil_dir}."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True)
        # Evil files must exit with 1 (reject)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}")