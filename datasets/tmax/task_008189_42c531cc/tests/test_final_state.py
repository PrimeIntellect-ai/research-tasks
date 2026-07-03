# test_final_state.py

import os
import subprocess
import difflib
import pytest

PROJECT_DIR = "/home/user/project"
EXPR_EVAL_C = os.path.join(PROJECT_DIR, "expr_eval.c")
LIBEXPR_EVAL_SO = os.path.join(PROJECT_DIR, "libexpr_eval.so")
RUN_TEST_PY = os.path.join(PROJECT_DIR, "run_test.py")
DIFF_LOG = os.path.join(PROJECT_DIR, "diff.log")
INPUT_TXT = os.path.join(PROJECT_DIR, "input.txt")
BASELINE_TXT = os.path.join(PROJECT_DIR, "baseline.txt")

def test_expr_eval_c_memory_fix():
    """Verify that the memory allocation bug in expr_eval.c has been fixed."""
    assert os.path.isfile(EXPR_EVAL_C), f"File {EXPR_EVAL_C} is missing."
    with open(EXPR_EVAL_C, "r") as f:
        content = f.read()

    # The original buggy code had: malloc(count)
    # The fix should include sizeof(int) or similar multiplier.
    assert "malloc(count)" not in content.replace(" ", ""), \
        "The memory allocation bug (malloc(count)) is still present in expr_eval.c."
    assert "sizeof" in content or "*" in content, \
        "The memory allocation in expr_eval.c does not appear to allocate enough space (missing sizeof multiplier)."

def test_libexpr_eval_so_compiled_and_linked_correctly():
    """Verify that libexpr_eval.so exists and does not export parse_op globally."""
    assert os.path.isfile(LIBEXPR_EVAL_SO), f"Shared library {LIBEXPR_EVAL_SO} was not compiled."

    try:
        # Check exported dynamic symbols
        output = subprocess.check_output(["nm", "-g", LIBEXPR_EVAL_SO], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run nm on {LIBEXPR_EVAL_SO}: {e.output}")

    # parse_op should not be exposed as a global symbol (it should be static or renamed)
    for line in output.splitlines():
        if " parse_op" in line:
            pytest.fail(f"Symbol 'parse_op' is still exported globally in {LIBEXPR_EVAL_SO}. It must be made static or encapsulated.")

def test_run_test_py_exists():
    """Verify that the Python script run_test.py was created."""
    assert os.path.isfile(RUN_TEST_PY), f"Python script {RUN_TEST_PY} is missing."

def test_diff_log_correctness():
    """Verify that diff.log contains the correct unified diff output."""
    assert os.path.isfile(DIFF_LOG), f"Diff log file {DIFF_LOG} is missing."

    # Recompute the expected results based on the task description
    # Input: 10+5=15, 20-3=17, 4*4=16, 18/2=9
    # Sorted: 9, 15, 16, 17
    expected_results = ["9\n", "15\n", "16\n", "17\n"]

    # Read baseline dynamically
    assert os.path.isfile(BASELINE_TXT), f"Baseline file {BASELINE_TXT} is missing."
    with open(BASELINE_TXT, "r") as f:
        baseline = f.readlines()

    # Generate the expected diff dynamically
    expected_diff_lines = list(difflib.unified_diff(
        baseline, 
        expected_results, 
        fromfile="baseline", 
        tofile="results"
    ))
    expected_diff_str = "".join(expected_diff_lines)

    # Read actual diff
    with open(DIFF_LOG, "r") as f:
        actual_diff_str = f.read()

    assert actual_diff_str.strip() == expected_diff_str.strip(), \
        f"Contents of {DIFF_LOG} do not match the expected unified diff.\nExpected:\n{expected_diff_str}\nActual:\n{actual_diff_str}"