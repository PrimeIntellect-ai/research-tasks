# test_final_state.py

import os
import subprocess
import pytest

def test_results_log_exists():
    log_path = "/home/user/test_results.log"
    assert os.path.exists(log_path), f"The log file {log_path} does not exist. Did you run the test suite and redirect the output?"
    assert os.path.isfile(log_path), f"{log_path} is not a valid file."

def test_results_log_contents():
    log_path = "/home/user/test_results.log"
    if not os.path.exists(log_path):
        pytest.fail(f"Log file {log_path} missing.")

    with open(log_path, "r") as f:
        content = f.read()

    assert "[PASS] Auth Test" in content, "Auth Test did not pass. Check your compare_versions logic."
    assert "[PASS] GraphQL Test" in content, "GraphQL Test did not pass. Check your generate_fuzz_length logic."
    assert "[PASS] REST Test" in content, "REST Test did not pass. Check your compare_versions logic."
    assert "[FAIL]" not in content, "There are still failing tests in the log output."

def test_run_tests_no_infinite_loop():
    script_path = "/home/user/sec_suite/run_tests.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."

    try:
        # Run the script with a short timeout to catch infinite recursion
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True,
            timeout=3
        )
        assert result.returncode == 0, f"Script failed to run with return code {result.returncode}. Error: {result.stderr}"
        assert "Starting Security Test Suite..." in result.stdout
        assert "Test Suite Completed." in result.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Running run_tests.sh timed out. The circular sourcing (infinite recursion) issue has not been fully resolved.")

def test_compare_versions_logic():
    utils_path = "/home/user/sec_suite/utils.sh"
    assert os.path.exists(utils_path), f"{utils_path} does not exist."

    test_cases = [
        ("1.2.10", "1.2.9", "1"),
        ("2.0.0", "2.0.0", "0"),
        ("1.9.9", "2.0.0", "-1"),
        ("0.0.1", "0.0.2", "-1"),
        ("10.0.0", "9.9.9", "1")
    ]

    for v1, v2, expected in test_cases:
        cmd = f"source {utils_path} && compare_versions {v1} {v2}"
        result = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
        output = result.stdout.strip()
        assert output == expected, f"compare_versions {v1} {v2} returned '{output}', expected '{expected}'"

def test_generate_fuzz_length_logic():
    utils_path = "/home/user/sec_suite/utils.sh"
    assert os.path.exists(utils_path), f"{utils_path} does not exist."

    test_cases = [
        ("0", "2"),
        ("1", "1"),
        ("2", "3"),
        ("3", "4"),
        ("4", "7"),
        ("7", "29"),
        ("10", "123")
    ]

    for n, expected in test_cases:
        cmd = f"source {utils_path} && generate_fuzz_length {n}"
        result = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
        output = result.stdout.strip()
        assert output == expected, f"generate_fuzz_length {n} returned '{output}', expected '{expected}'"