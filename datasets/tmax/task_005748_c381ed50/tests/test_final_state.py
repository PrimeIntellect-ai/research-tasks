# test_final_state.py
import os
import re

WORKSPACE_DIR = "/home/user/workspace"
LIB_PATH = os.path.join(WORKSPACE_DIR, "libpricing.so")
RUN_ALL_PATH = os.path.join(WORKSPACE_DIR, "run_all.sh")
TEST_REPORT_PATH = os.path.join(WORKSPACE_DIR, "test_report.log")
TEST_SERVER_PATH = os.path.join(WORKSPACE_DIR, "test_server.py")
SERVER_PATH = os.path.join(WORKSPACE_DIR, "server.py")

def test_shared_library_exists():
    assert os.path.isfile(LIB_PATH), f"Shared library {LIB_PATH} was not created."
    # Basic check for ELF shared object signature
    with open(LIB_PATH, "rb") as f:
        header = f.read(4)
        assert header == b"\x7fELF", f"{LIB_PATH} is not a valid ELF file."

def test_run_all_script_exists():
    assert os.path.isfile(RUN_ALL_PATH), f"Shell script {RUN_ALL_PATH} is missing."

def test_test_report_exists_and_passed():
    assert os.path.isfile(TEST_REPORT_PATH), f"Test report {TEST_REPORT_PATH} is missing."
    with open(TEST_REPORT_PATH, "r") as f:
        content = f.read()

    # Look for pytest success output, e.g., "1 passed" or "passed"
    assert re.search(r'\bpassed\b', content.lower()), "Test report does not indicate passing tests."

def test_test_server_uses_patch():
    assert os.path.isfile(TEST_SERVER_PATH), f"Test file {TEST_SERVER_PATH} is missing."
    with open(TEST_SERVER_PATH, "r") as f:
        content = f.read()

    assert "patch" in content, f"{TEST_SERVER_PATH} does not seem to use mock.patch."

def test_server_uses_cdll():
    assert os.path.isfile(SERVER_PATH), f"Server file {SERVER_PATH} is missing."
    with open(SERVER_PATH, "r") as f:
        content = f.read()

    assert "CDLL" in content, f"{SERVER_PATH} does not seem to use ctypes.CDLL to load the shared library."