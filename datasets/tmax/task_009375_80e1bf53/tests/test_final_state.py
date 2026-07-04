# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
LIBWEB_SO = os.path.join(PROJECT_DIR, "libweb.so")
TEST_DEPLOY = os.path.join(PROJECT_DIR, "test_deploy")
DEPLOYMENT_LOG = "/home/user/deployment_log.txt"

def test_libweb_so_exists_and_shared():
    assert os.path.isfile(LIBWEB_SO), f"Shared library {LIBWEB_SO} is missing."

    # Check if it is a shared object using the 'file' command
    result = subprocess.run(["file", LIBWEB_SO], capture_output=True, text=True)
    assert "shared object" in result.stdout.lower() or "dynamically linked" in result.stdout.lower(), \
        f"{LIBWEB_SO} does not appear to be a shared object. Output: {result.stdout}"

def test_test_deploy_exists_and_linked():
    assert os.path.isfile(TEST_DEPLOY), f"Executable {TEST_DEPLOY} is missing."
    assert os.access(TEST_DEPLOY, os.X_OK), f"File {TEST_DEPLOY} is not executable."

    # Check if it is dynamically linked to libweb.so using ldd
    result = subprocess.run(["ldd", TEST_DEPLOY], capture_output=True, text=True)
    assert "libweb.so" in result.stdout, \
        f"{TEST_DEPLOY} is not dynamically linked to libweb.so. ldd output: {result.stdout}"

def test_deployment_log_content():
    assert os.path.isfile(DEPLOYMENT_LOG), f"Deployment log {DEPLOYMENT_LOG} is missing."

    with open(DEPLOYMENT_LOG, "r") as f:
        content = f.read()

    expected_content = "api/v1/data%20view"
    assert content == expected_content, \
        f"Content of {DEPLOYMENT_LOG} is incorrect. Expected '{expected_content}', got '{content}'."