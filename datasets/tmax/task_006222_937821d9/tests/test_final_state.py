# test_final_state.py

import os
import subprocess
import pytest

PAYLOAD_FILE = "/home/user/injected_payload.txt"
TEST_SCRIPT = "/home/user/test_artifact.sh"

def test_injected_payload_file():
    assert os.path.isfile(PAYLOAD_FILE), f"File {PAYLOAD_FILE} does not exist."
    with open(PAYLOAD_FILE, "rb") as f:
        content = f.read()

    # The string could be written as literal \r\n or actual CR LF bytes.
    # The core string must be present.
    assert b"X-Malicious-Backdoor: active" in content, f"The payload file does not contain the expected malicious header string."

def test_test_artifact_script_exists_and_executable():
    assert os.path.isfile(TEST_SCRIPT), f"Script {TEST_SCRIPT} does not exist."
    assert os.access(TEST_SCRIPT, os.X_OK), f"Script {TEST_SCRIPT} is not executable."

def test_test_artifact_script_execution():
    # Run the test script and assert it exits with code 0
    try:
        result = subprocess.run([TEST_SCRIPT], capture_output=True, text=True, timeout=5)
    except Exception as e:
        pytest.fail(f"Failed to execute {TEST_SCRIPT}: {e}")

    assert result.returncode == 0, f"{TEST_SCRIPT} failed with exit code {result.returncode}. Stderr: {result.stderr}"