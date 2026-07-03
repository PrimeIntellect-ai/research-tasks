# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/ci_test.sh"
BUILD_DIR = "/home/user/build"
LIB_PATH = os.path.join(BUILD_DIR, "libcompute.so")
APP_PATH = os.path.join(BUILD_DIR, "app")
DB_PATH = os.path.join(BUILD_DIR, "app.db")
LOG_PATH = "/home/user/test_result.log"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution():
    # Execute the script
    result = subprocess.run(
        ["bash", SCRIPT_PATH],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_build_artifacts_exist():
    assert os.path.isfile(LIB_PATH), f"Shared library {LIB_PATH} was not created."
    assert os.path.isfile(APP_PATH), f"Executable {APP_PATH} was not created."
    assert os.path.isfile(DB_PATH), f"Database {DB_PATH} was not created."

def test_test_result_log():
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} was not created."
    with open(LOG_PATH, "r") as f:
        content = f.read().strip()

    expected_output = "MIGRATED_HASH=630"
    assert content == expected_output, f"Expected log content '{expected_output}', but got '{content}'."