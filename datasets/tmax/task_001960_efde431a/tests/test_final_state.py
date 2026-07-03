# test_final_state.py

import os
import pytest

def test_http_fuzzer_compiled():
    """Verify the http_fuzzer compiled successfully and is executable."""
    path = "/home/user/tool/http_fuzzer"
    assert os.path.isfile(path), f"Executable not found: {path}. The Makefile might still be broken or the build failed."
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_test_result_log_exists():
    """Verify the E2E test script output was redirected to test_result.log."""
    path = "/home/user/test_result.log"
    assert os.path.isfile(path), f"Log file not found: {path}. Did you run the e2e_test.sh script and redirect its output?"

def test_test_result_log_content_payload():
    """Check that the log contains the successfully returned string from the Rust binary."""
    path = "/home/user/test_result.log"
    if not os.path.exists(path):
        pytest.fail(f"Cannot check content because {path} does not exist.")

    with open(path, "r") as f:
        content = f.read()

    expected_str = "Fuzzer sending payload: FUZZ_PAYLOAD_X99"
    assert expected_str in content, f"Log does not contain expected payload output. The Rust bug might not be correctly fixed. Expected to find: '{expected_str}'"

def test_test_result_log_content_success():
    """Check that the log contains the completion string."""
    path = "/home/user/test_result.log"
    if not os.path.exists(path):
        pytest.fail(f"Cannot check content because {path} does not exist.")

    with open(path, "r") as f:
        content = f.read()

    expected_str = "E2E Test Complete. Success!"
    assert expected_str in content, f"Log does not contain the success message. The E2E script may have failed. Expected to find: '{expected_str}'"