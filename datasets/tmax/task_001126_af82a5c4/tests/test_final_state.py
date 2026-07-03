# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/filter_model/target/release/filter_model"
CLEAN_DIR = "/app/data/clean/"
EVIL_DIR = "/app/data/evil/"

def test_binary_exists():
    assert os.path.exists(BINARY_PATH), f"Binary not found at {BINARY_PATH}"
    assert os.path.isfile(BINARY_PATH), f"Path {BINARY_PATH} is not a file"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_clean_corpus():
    assert os.path.exists(CLEAN_DIR), f"Clean directory {CLEAN_DIR} is missing"

    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    assert len(files) > 0, f"No CSV files found in {CLEAN_DIR}"

    failed_files = []
    for file in files:
        filepath = os.path.join(CLEAN_DIR, file)
        try:
            res = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True, timeout=5)
            output = res.stdout.strip()
            if output != "CLEAN":
                failed_files.append((file, output))
        except Exception as e:
            failed_files.append((file, str(e)))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(files)} clean modified/rejected.\n"
        error_msg += "Offending files:\n"
        for f, out in failed_files:
            error_msg += f"  {f}: got '{out}'\n"
        pytest.fail(error_msg)

def test_evil_corpus():
    assert os.path.exists(EVIL_DIR), f"Evil directory {EVIL_DIR} is missing"

    files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    assert len(files) > 0, f"No CSV files found in {EVIL_DIR}"

    failed_files = []
    for file in files:
        filepath = os.path.join(EVIL_DIR, file)
        try:
            res = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True, timeout=5)
            output = res.stdout.strip()
            if output != "EVIL":
                failed_files.append((file, output))
        except Exception as e:
            failed_files.append((file, str(e)))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(files)} evil bypassed.\n"
        error_msg += "Offending files:\n"
        for f, out in failed_files:
            error_msg += f"  {f}: got '{out}'\n"
        pytest.fail(error_msg)