# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detector.sh"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_detector_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_clean_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean directory {CLEAN_DIR} is missing."

    files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(files) > 0, "No clean databases found."

    failed_files = []
    for f in files:
        db_path = os.path.join(CLEAN_DIR, f)
        result = subprocess.run([SCRIPT_PATH, db_path], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 0 or output != "CLEAN":
            failed_files.append((f, result.returncode, output))

    if failed_files:
        msg = f"{len(failed_files)} of {len(files)} clean modified (rejected).\n"
        for f, rc, out in failed_files:
            msg += f"File: {f}, Exit code: {rc}, Output: '{out}'\n"
        pytest.fail(msg)

def test_evil_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil directory {EVIL_DIR} is missing."

    files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(files) > 0, "No evil databases found."

    failed_files = []
    for f in files:
        db_path = os.path.join(EVIL_DIR, f)
        result = subprocess.run([SCRIPT_PATH, db_path], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 1 or output != "CORRUPTED":
            failed_files.append((f, result.returncode, output))

    if failed_files:
        msg = f"{len(failed_files)} of {len(files)} evil bypassed.\n"
        for f, rc, out in failed_files:
            msg += f"File: {f}, Exit code: {rc}, Output: '{out}'\n"
        pytest.fail(msg)