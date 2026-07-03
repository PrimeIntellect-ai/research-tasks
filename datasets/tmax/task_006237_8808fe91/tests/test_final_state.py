# test_final_state.py

import os
import subprocess
import pytest

def test_api_parser_compiled_and_executable():
    """Verify that the C program was compiled to the correct path and is executable."""
    executable_path = "/home/user/api_parser"
    assert os.path.isfile(executable_path), f"Compiled binary {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"Compiled binary {executable_path} is not executable."

def test_api_parser_c_modified_for_bounds_checking():
    """Verify that the C source code was modified to cap the length to 49."""
    source_path = "/home/user/api_parser.c"
    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."

    with open(source_path, "r") as f:
        content = f.read()

    # Check if the code has some logic to cap the length at 49
    # We won't strictly check the exact syntax, but '49' should be present in the file
    assert "49" in content, "The C source code does not seem to contain the logic to cap the length to 49."

def test_api_parser_no_segfault_on_large_payload(tmp_path):
    """Verify that the compiled binary no longer segfaults on a payload > 49 bytes."""
    executable_path = "/home/user/api_parser"
    test_bin = tmp_path / "check.bin"

    # Create a test file with length byte 255 followed by 255 'A's
    with open(test_bin, "wb") as f:
        f.write(b'\xff' + b'A' * 255)

    try:
        result = subprocess.run([executable_path, str(test_bin)], capture_output=True, timeout=2)
        assert result.returncode == 0, f"Expected exit code 0, but got {result.returncode}. The program might still be crashing."
    except subprocess.TimeoutExpired:
        pytest.fail("The compiled program timed out.")
    except Exception as e:
        pytest.fail(f"Failed to execute the compiled program: {e}")

def test_fuzz_script_exists():
    """Verify that the fuzzing script exists."""
    script_path = "/home/user/fuzz.sh"
    assert os.path.isfile(script_path), f"Fuzzing script {script_path} does not exist."

def test_fuzz_result_log():
    """Verify that the fuzz result log exists and contains 'SUCCESS'."""
    log_path = "/home/user/fuzz_result.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the fuzzer?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "SUCCESS" in content, f"Log file {log_path} does not contain 'SUCCESS'. Found: {content}"