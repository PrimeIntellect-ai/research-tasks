# test_final_state.py

import os
import zlib
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/api_workspace"
PAYLOAD_FILE = os.path.join(WORKSPACE_DIR, "payload.dat")
API_TESTER_FILE = os.path.join(WORKSPACE_DIR, "api_tester.c")
BUILD_SH_FILE = os.path.join(WORKSPACE_DIR, "build.sh")
RUN_TESTS_SH_FILE = os.path.join(WORKSPACE_DIR, "run_tests.sh")
LOG_FILE = "/home/user/test_results.log"

def get_expected_crc32():
    with open(PAYLOAD_FILE, "rb") as f:
        data = f.read()
    # zlib.crc32 returns an unsigned 32-bit integer
    crc = zlib.crc32(data) & 0xFFFFFFFF
    return f"{crc:08x}"

def test_payload_not_modified():
    assert os.path.isfile(PAYLOAD_FILE), f"Payload file {PAYLOAD_FILE} is missing."
    with open(PAYLOAD_FILE, "r") as f:
        content = f.read()
    assert content == "INTEGRATION_TEST_PAYLOAD_V1", "payload.dat was modified, which is forbidden."

def test_build_sh_fixed():
    assert os.path.isfile(BUILD_SH_FILE), f"{BUILD_SH_FILE} is missing."
    with open(BUILD_SH_FILE, "r") as f:
        content = f.read()
    assert "-lz" in content, f"{BUILD_SH_FILE} does not link zlib (-lz). The build will fail."

def test_run_tests_sh_exists_and_executable():
    assert os.path.isfile(RUN_TESTS_SH_FILE), f"{RUN_TESTS_SH_FILE} was not created."
    assert os.access(RUN_TESTS_SH_FILE, os.X_OK), f"{RUN_TESTS_SH_FILE} does not have executable permissions."

def test_execution_and_results():
    # Remove log file if it exists to ensure we are testing the script's creation of it
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # Run the student's script
    result = subprocess.run(
        ["./run_tests.sh"],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run_tests.sh failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} was not created by run_tests.sh."

    with open(LOG_FILE, "r") as f:
        actual_content = f.read().strip()

    expected_checksum = get_expected_crc32()
    assert actual_content == expected_checksum, (
        f"The test results log should contain ONLY the checksum '{expected_checksum}', "
        f"but found '{actual_content}'."
    )