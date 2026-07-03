# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/ci_cd_test"

def test_pqueue_app_compiled():
    app_path = os.path.join(BASE_DIR, "pqueue_app")
    assert os.path.isfile(app_path), f"Executable {app_path} does not exist. The Makefile was likely not fixed or 'make' was not run."
    assert os.access(app_path, os.X_OK), f"File {app_path} is not executable."

def test_bash_script_fixed():
    script_path = os.path.join(BASE_DIR, "run_tests.sh")
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "declare -A test_cases" in content, "run_tests.sh does not contain 'declare -A test_cases'. The associative array declaration was not fixed."
    assert "declare -a test_cases" not in content, "run_tests.sh still contains the broken 'declare -a test_cases'."

def test_test_report_generated_and_correct():
    report_path = os.path.join(BASE_DIR, "test_report.txt")
    assert os.path.isfile(report_path), f"Test report {report_path} does not exist. Did you redirect the output of run_tests.sh?"

    with open(report_path, "r") as f:
        content = f.read()

    expected_lines = [
        "Test 'push 5 push 10 pop' - PASS",
        "Test 'push 1 pop pop' - PASS",
        "Test 'push 20 push 5 push 30 pop pop' - PASS"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {report_path}. The tests might have failed or the report is incomplete."