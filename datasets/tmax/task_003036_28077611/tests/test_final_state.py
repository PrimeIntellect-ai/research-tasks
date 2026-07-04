# test_final_state.py

import os
import subprocess
import pytest

APP_DIR = "/home/user/app"
MOCK_C = os.path.join(APP_DIR, "mock_crypto.c")
MOCK_SO = os.path.join(APP_DIR, "libmock_crypto.so")
TEST_SH = os.path.join(APP_DIR, "test_fixture.sh")
TEST_LOG = os.path.join(APP_DIR, "test_result.log")

def test_mock_c_exists():
    assert os.path.isfile(MOCK_C), f"Expected {MOCK_C} to exist."

def test_mock_so_exists():
    assert os.path.isfile(MOCK_SO), f"Expected {MOCK_SO} to exist."

def test_test_fixture_exists_and_executable():
    assert os.path.isfile(TEST_SH), f"Expected {TEST_SH} to exist."
    assert os.access(TEST_SH, os.X_OK), f"Expected {TEST_SH} to be executable."

def test_test_result_log_contents():
    # It's possible the student hasn't run the script themselves, but the instructions say
    # "The test_fixture.sh script must capture...". We should run it to be sure, or just check
    # if it exists and contains the expected output if they ran it.
    # The instructions say "Write a Bash script... that runs... and saves it exactly to...".
    # Let's run the script to ensure it creates/updates the log properly.

    # Remove log if it exists to ensure the script creates it
    if os.path.exists(TEST_LOG):
        os.remove(TEST_LOG)

    result = subprocess.run([TEST_SH], cwd=APP_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"{TEST_SH} failed to execute properly. Stderr: {result.stderr}"

    assert os.path.isfile(TEST_LOG), f"{TEST_LOG} was not created by {TEST_SH}."

    with open(TEST_LOG, "r") as f:
        content = f.read()

    assert "Authentication Success" in content, f"Expected 'Authentication Success' in {TEST_LOG}, but got: {content}"

def test_mock_so_exports_verify_signature():
    # Verify that the shared object actually exports verify_signature
    result = subprocess.run(["nm", "-D", MOCK_SO], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run nm on {MOCK_SO}"
    assert "verify_signature" in result.stdout, f"verify_signature symbol not found in {MOCK_SO}"