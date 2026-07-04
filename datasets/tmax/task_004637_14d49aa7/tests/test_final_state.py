# test_final_state.py

import os
import pytest

PIPELINE_DIR = "/home/user/pipeline"
CALC_C = os.path.join(PIPELINE_DIR, "calc.c")
MAKEFILE = os.path.join(PIPELINE_DIR, "Makefile")
CI_TEST_SH = os.path.join(PIPELINE_DIR, "ci_test.sh")
CI_REPORT_TXT = os.path.join(PIPELINE_DIR, "ci_report.txt")

def test_makefile_contains_debug_symbols():
    assert os.path.isfile(MAKEFILE), f"Makefile not found at {MAKEFILE}"
    with open(MAKEFILE, "r") as f:
        content = f.read()
    assert "-g" in content, "Makefile does not contain the '-g' flag for debugging symbols."

def test_ci_test_sh_exists():
    assert os.path.isfile(CI_TEST_SH), f"Test orchestration script not found at {CI_TEST_SH}"

def test_ci_report_contents():
    assert os.path.isfile(CI_REPORT_TXT), f"Report file not found at {CI_REPORT_TXT}"

    expected_lines = [
        "[1] result=15 status=PASS",
        "[3] result=11 status=PASS",
        "[5] result=50 status=PASS"
    ]

    with open(CI_REPORT_TXT, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {CI_REPORT_TXT} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_calc_c_fixed():
    assert os.path.isfile(CALC_C), f"calc.c not found at {CALC_C}"
    with open(CALC_C, "r") as f:
        content = f.read()
    # A simple check to ensure some form of free() is now present
    assert "free(" in content, "calc.c does not seem to contain a call to free() to fix the memory leak."