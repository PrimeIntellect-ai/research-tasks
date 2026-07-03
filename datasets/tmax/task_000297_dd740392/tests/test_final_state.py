# test_final_state.py
import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/vm_project"
EXECUTABLE = os.path.join(PROJECT_DIR, "simple_vm")
REPORT_JSON = os.path.join(PROJECT_DIR, "report.json")
TEST_RUNNER = os.path.join(PROJECT_DIR, "test_runner.py")

def test_executable_compiles_and_exists():
    """Check that the simple_vm executable exists (meaning compilation succeeded)."""
    # First, let's try to run make just in case it wasn't run, 
    # but the prompt says 'leave the compiled executable'.
    # We will just check if the executable exists.
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} is missing. Did the code compile successfully?"
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_vm_behavior_normal():
    """Test that the VM correctly executes a normal program."""
    test_file = os.path.join(PROJECT_DIR, "tests", "test_normal.asm")
    result = subprocess.run([EXECUTABLE, test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Expected exit code 0 for normal program, got {result.returncode}"
    assert result.stdout.strip() == "15", f"Expected output '15', got '{result.stdout.strip()}'"

def test_vm_behavior_overflow():
    """Test that the VM correctly handles stack overflow."""
    test_file = os.path.join(PROJECT_DIR, "tests", "test_overflow.asm")
    result = subprocess.run([EXECUTABLE, test_file], capture_output=True, text=True)
    assert result.returncode == 1, f"Expected exit code 1 for stack overflow, got {result.returncode}"
    assert result.stdout.strip() == "Error: Stack Overflow", f"Expected 'Error: Stack Overflow', got '{result.stdout.strip()}'"

def test_vm_behavior_underflow():
    """Test that the VM correctly handles stack underflow."""
    test_file = os.path.join(PROJECT_DIR, "tests", "test_underflow.asm")
    result = subprocess.run([EXECUTABLE, test_file], capture_output=True, text=True)
    assert result.returncode == 1, f"Expected exit code 1 for stack underflow, got {result.returncode}"
    assert result.stdout.strip() == "Error: Stack Underflow", f"Expected 'Error: Stack Underflow', got '{result.stdout.strip()}'"

def test_test_runner_exists():
    """Check that the Python test runner script exists."""
    assert os.path.isfile(TEST_RUNNER), f"Test runner script {TEST_RUNNER} is missing."

def test_report_json_exists_and_correct():
    """Check that report.json exists and contains the expected test results."""
    assert os.path.isfile(REPORT_JSON), f"Report file {REPORT_JSON} is missing."

    try:
        with open(REPORT_JSON, "r") as f:
            report = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{REPORT_JSON} does not contain valid JSON.")

    expected_results = {
        "test_normal.asm": "pass",
        "test_overflow.asm": "pass",
        "test_underflow.asm": "pass"
    }

    for test_file, expected_status in expected_results.items():
        assert test_file in report, f"Test file {test_file} is missing from {REPORT_JSON}"
        assert report[test_file] == expected_status, f"Expected {test_file} to be '{expected_status}', got '{report[test_file]}'"