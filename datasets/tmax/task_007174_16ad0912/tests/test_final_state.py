# test_final_state.py

import os
import stat
import pytest

API_PROJECT_DIR = "/home/user/api_project"
ROUTER_EXEC_PATH = os.path.join(API_PROJECT_DIR, "router")
RUN_TESTS_SH_PATH = os.path.join(API_PROJECT_DIR, "run_tests.sh")
TEST_REPORT_PATH = os.path.join(API_PROJECT_DIR, "test_report.log")

EXPECTED_REPORT = """SUCCESS - /api/v1/health -> Route: /api/v1/health Params: NONE
SUCCESS - /api/v2/users?active=true&sort=desc -> Route: /api/v2/users Params: active=true&sort=desc
FAILURE - malformed/url/path -> INVALID_ROUTE
SUCCESS - /webhooks/stripe?sig=xyz123 -> Route: /webhooks/stripe Params: sig=xyz123
FAILURE - admin/dashboard -> INVALID_ROUTE
SUCCESS - / -> Route: / Params: NONE
"""

def test_router_executable_exists():
    assert os.path.isfile(ROUTER_EXEC_PATH), f"Executable {ROUTER_EXEC_PATH} was not built."
    assert os.access(ROUTER_EXEC_PATH, os.X_OK), f"{ROUTER_EXEC_PATH} is not executable."

def test_run_tests_sh_exists_and_executable():
    assert os.path.isfile(RUN_TESTS_SH_PATH), f"Script {RUN_TESTS_SH_PATH} does not exist."
    st = os.stat(RUN_TESTS_SH_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {RUN_TESTS_SH_PATH} is not executable."

def test_test_report_log_matches():
    assert os.path.isfile(TEST_REPORT_PATH), f"Report file {TEST_REPORT_PATH} does not exist."
    with open(TEST_REPORT_PATH, "r") as f:
        actual_report = f.read()

    # Strip trailing newlines for a robust comparison
    actual_lines = [line.strip() for line in actual_report.strip().split("\n")]
    expected_lines = [line.strip() for line in EXPECTED_REPORT.strip().split("\n")]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in test_report.log, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i+1} of test_report.log.\nExpected: {expected}\nGot: {actual}"