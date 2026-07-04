# test_final_state.py
import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/etl_filter.sh"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS, "*.csv"))
    assert len(clean_files) > 0, f"No clean CSV files found in {CLEAN_CORPUS}."

    failed_files = []
    for csv_file in clean_files:
        result = subprocess.run([SCRIPT_PATH, csv_file], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (should be accepted). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS, "*.csv"))
    assert len(evil_files) > 0, f"No evil CSV files found in {EVIL_CORPUS}."

    bypassed_files = []
    for csv_file in evil_files:
        result = subprocess.run([SCRIPT_PATH, csv_file], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(csv_file))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed (should be rejected). Offending files: {', '.join(bypassed_files)}")