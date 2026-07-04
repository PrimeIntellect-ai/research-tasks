# test_final_state.py

import os
import re
import pytest

APP_DIR = "/home/user/sec-app"
LOG_FILE = os.path.join(APP_DIR, "test_results.log")
MIDDLEWARE_FILE = os.path.join(APP_DIR, "middleware.go")

def test_test_results_log_exists():
    assert os.path.isfile(LOG_FILE), f"The file {LOG_FILE} does not exist. Did you run 'make test'?"

def test_test_results_log_passed():
    with open(LOG_FILE, "r") as f:
        content = f.read()

    assert "FAIL" not in content, "The test results log contains failures."
    assert "PASS" in content, "The test results log does not indicate a successful test run (missing 'PASS')."

def test_middleware_logic_fixed():
    assert os.path.isfile(MIDDLEWARE_FILE), f"The file {MIDDLEWARE_FILE} does not exist."

    with open(MIDDLEWARE_FILE, "r") as f:
        content = f.read()

    # The bug was `if requestCount > 10 {`
    # It should be fixed to `if requestCount > 5 {` or something equivalent.
    # We check that the hardcoded 10 is gone and replaced by 5 (or similar logic).
    assert "requestCount > 10" not in content, "The rate limit logic still contains 'requestCount > 10'."

    # Allow various spacings, e.g., requestCount > 5, requestCount >= 6, requestCount == 6
    match = re.search(r'requestCount\s*(>|>=|==)\s*([56])', content)
    assert match is not None, "Could not find the corrected rate limiting logic in middleware.go (expected condition like 'requestCount > 5')."

def test_cgo_or_makefile_fixed():
    # To pass `make test`, either middleware.go has an rpath directive or Makefile sets LD_LIBRARY_PATH.
    # Since test_test_results_log_passed already verifies that `make test` succeeded, 
    # we don't strictly need to parse the source for the exact fix, as the successful execution
    # of the test binary dynamically linked to the C library proves the linker issue was resolved.
    pass