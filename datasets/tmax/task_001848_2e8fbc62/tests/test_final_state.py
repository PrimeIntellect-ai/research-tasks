# test_final_state.py

import os
import subprocess
import pytest

def test_build_script_exists_and_executable():
    script_path = "/home/user/app/build_and_test.sh"
    assert os.path.isfile(script_path), f"Build script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Build script {script_path} is not executable."

def test_binary_exists_and_executable():
    bin_path = "/home/user/app/bin/sanitize"
    assert os.path.isfile(bin_path), f"Binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

    # Check if it's an ELF file
    with open(bin_path, 'rb') as f:
        magic = f.read(4)
        assert magic == b'\x7fELF', f"File {bin_path} is not a valid ELF executable."

def test_test_results_log():
    log_path = "/home/user/app/test_results.log"
    assert os.path.isfile(log_path), f"Test results log {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    # Pytest output should indicate 2 passed tests
    assert "2 passed" in content, "test_results.log does not indicate that 2 tests passed."

def test_sanitize_binary_execution():
    bin_path = "/home/user/app/bin/sanitize"
    long_string = "this_is_a_very_long_string_that_needs_to_be_sanitized_without_crashing_the_backend_service"

    try:
        result = subprocess.run([bin_path, long_string], capture_output=True, text=True, timeout=2)
    except Exception as e:
        pytest.fail(f"Failed to execute {bin_path}: {e}")

    assert result.returncode == 0, f"Binary crashed or exited with non-zero code: {result.returncode}"

    expected_output = f"CLEAN: {long_string}"
    stdout_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    # The output should contain the expected output
    assert expected_output in stdout_lines, f"Expected output '{expected_output}' not found in binary stdout: {result.stdout}"