# test_final_state.py

import os
import subprocess
import pytest

REPO_DIR = "/home/user/fast-telemetry"
TEST_RESULTS_LOG = "/home/user/test_results.log"

def test_branch_checked_out():
    """Ensure the correct branch is checked out."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    branch = result.stdout.strip()
    assert branch == "pr-104-fast-delta", f"Expected branch 'pr-104-fast-delta', but got '{branch}'"

def test_test_results_log():
    """Ensure test_results.log exists and contains 'ALL TESTS PASSED'."""
    assert os.path.isfile(TEST_RESULTS_LOG), f"{TEST_RESULTS_LOG} does not exist."
    with open(TEST_RESULTS_LOG, "r") as f:
        content = f.read()
    assert "ALL TESTS PASSED" in content, f"'{TEST_RESULTS_LOG}' does not contain 'ALL TESTS PASSED'."

def test_delta_calc_fixed():
    """Ensure delta_calc.c uses subl instead of addl."""
    delta_calc_path = os.path.join(REPO_DIR, "src", "delta_calc.c")
    assert os.path.isfile(delta_calc_path), f"{delta_calc_path} does not exist."
    with open(delta_calc_path, "r") as f:
        content = f.read()
    assert "subl" in content, "delta_calc.c does not contain 'subl'. The assembly was not fixed."
    assert "addl" not in content.split("//")[0], "delta_calc.c still contains 'addl' in the assembly."

def test_make_test_passes():
    """Ensure 'make test' compiles and runs successfully without modifying /etc/telemetry.log."""
    # Run make clean to ensure a fresh build
    subprocess.run(["make", "clean"], cwd=REPO_DIR, check=True)

    # Run make test
    result = subprocess.run(
        ["make", "test"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'make test' failed with output:\n{result.stdout}\n{result.stderr}"
    assert "ALL TESTS PASSED" in result.stdout, "'make test' output does not contain 'ALL TESTS PASSED'."

def test_mock_sink_used():
    """Ensure tests/test_main.c uses mock_output and does not use /etc/telemetry.log."""
    test_main_path = os.path.join(REPO_DIR, "tests", "test_main.c")
    assert os.path.isfile(test_main_path), f"{test_main_path} does not exist."
    with open(test_main_path, "r") as f:
        content = f.read()

    assert "mock_output" in content, "test_main.c does not contain 'mock_output' as requested."
    assert "/etc/telemetry.log" not in content, "test_main.c still contains references to '/etc/telemetry.log'."