# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/calcgraph"
RESULTS_LOG = "/home/user/results.log"
RUN_TESTS_SH = os.path.join(BASE_DIR, "run_tests.sh")

def test_build_succeeds():
    """Ensure that running make succeeds, implying missing includes and Makefile are fixed."""
    # Clean first
    subprocess.run(["make", "clean"], cwd=BASE_DIR, capture_output=True)

    # Run make
    result = subprocess.run(["make"], cwd=BASE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with output:\n{result.stderr}\n{result.stdout}"

    # Check if executable exists
    executable_path = os.path.join(BASE_DIR, "calcgraph")
    assert os.path.isfile(executable_path), "calcgraph executable was not created by make."

def test_eval_c_fixed():
    """Ensure the logic bug in eval.c is fixed for OP_MUL."""
    eval_c_path = os.path.join(BASE_DIR, "eval.c")
    assert os.path.isfile(eval_c_path), f"File {eval_c_path} is missing."

    with open(eval_c_path, "r") as f:
        content = f.read()

    # Check that OP_MUL uses multiplication
    # We look for OP_MUL and an asterisk in the same line or generally check that left_val * right_val is present.
    assert "left_val * right_val" in content or "*" in content.split("OP_MUL")[1].split("\n")[0], \
        "eval.c does not seem to use '*' for OP_MUL. The logic bug is not fixed."

def test_run_tests_sh_exists_and_executable():
    """Ensure run_tests.sh exists and is executable."""
    assert os.path.isfile(RUN_TESTS_SH), f"Script {RUN_TESTS_SH} does not exist."
    assert os.access(RUN_TESTS_SH, os.X_OK), f"Script {RUN_TESTS_SH} is not executable."

def test_results_log_matches_expected():
    """Ensure results.log exists and contains exactly the expected output."""
    # We run the script to ensure it generates the correct file, but the prompt says 
    # we should check the final state. We will just check the file if it exists, 
    # and maybe run the script if the file isn't there, or just assume the user ran it.
    # The prompt says "after the student has completed the task", so the file should exist.
    assert os.path.isfile(RESULTS_LOG), f"{RESULTS_LOG} does not exist. Did the script run?"

    with open(RESULTS_LOG, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n")]

    expected_lines = [
        "test1: 25",
        "test2: 42",
        "test3: 95"
    ]

    assert len(lines) == 3, f"{RESULTS_LOG} should contain exactly 3 lines, found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in {RESULTS_LOG} is '{lines[i]}', expected '{expected}'."