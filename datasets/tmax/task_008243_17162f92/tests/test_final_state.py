# test_final_state.py

import os
import stat
import pytest

SCRIPT_PATH = "/home/user/compress_logs.sh"
LOGS_DIR = "/home/user/logs"
FILE_1 = os.path.join(LOGS_DIR, "app1.log")
FILE_2 = os.path.join(LOGS_DIR, "app2.log")
FILE_3 = os.path.join(LOGS_DIR, "app3.log")

EXPECTED_CONTENT_1 = """INFO: Service started
DATA: 10X5Y10Z
ERROR: Disk full warning
DATA: 1005150
INFO: Retrying operation
"""

EXPECTED_CONTENT_2 = """DATA: 50A
INFO: Done
DATA: 1A1B1C
"""

EXPECTED_CONTENT_3 = """INFO: Nothing to see here
ERROR: No data
"""

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_contains_required_commands():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    # Check for flock
    assert "flock" in content, "The script must use 'flock' to obtain an exclusive file lock."
    # Check for mv
    assert "mv" in content, "The script must use 'mv' to atomically replace the original file."

def test_app1_log_compressed():
    assert os.path.isfile(FILE_1), f"File {FILE_1} is missing."
    with open(FILE_1, 'r') as f:
        content = f.read()
    assert content == EXPECTED_CONTENT_1, f"Content of {FILE_1} does not match expected compressed state."

def test_app2_log_compressed():
    assert os.path.isfile(FILE_2), f"File {FILE_2} is missing."
    with open(FILE_2, 'r') as f:
        content = f.read()
    assert content == EXPECTED_CONTENT_2, f"Content of {FILE_2} does not match expected compressed state."

def test_app3_log_compressed():
    assert os.path.isfile(FILE_3), f"File {FILE_3} is missing."
    with open(FILE_3, 'r') as f:
        content = f.read()
    assert content == EXPECTED_CONTENT_3, f"Content of {FILE_3} does not match expected compressed state."