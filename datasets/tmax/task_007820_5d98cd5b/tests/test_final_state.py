# test_final_state.py

import os
import re

PROJECT_DIR = "/home/user/project"

def test_mathparser_h_fixed():
    path = os.path.join(PROJECT_DIR, "include", "mathparser.h")
    assert os.path.isfile(path), f"Header file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert 'extern "C"' in content, (
        f"The file {path} does not contain 'extern \"C\"'. "
        "This is required to fix the C/C++ linkage issue."
    )

def test_mathparser_c_fixed():
    path = os.path.join(PROJECT_DIR, "c_src", "mathparser.c")
    assert os.path.isfile(path), f"C source file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check that the bug 'a / b' is removed and replaced with 'b / a' or similar valid logic.
    # We look for the division operation.
    assert re.search(r'b\s*/\s*a', content) is not None, (
        f"The file {path} does not seem to have the division bug fixed. "
        "Expected to find 'b / a' (or equivalent) for the division operation."
    )
    assert re.search(r'a\s*/\s*b', content) is None, (
        f"The file {path} still contains the buggy 'a / b' division logic."
    )

def test_ci_success_log():
    log_path = os.path.join(PROJECT_DIR, "ci_success.log")
    assert os.path.isfile(log_path), (
        f"The log file {log_path} does not exist. "
        "Did you redirect the output of 'make ci' to this file?"
    )

    with open(log_path, "r") as f:
        content = f.read()

    expected_output = "PASS: 10 2 / = 5.0"
    assert expected_output in content, (
        f"The log file {log_path} does not contain the expected success output: '{expected_output}'. "
        "Make sure the tests passed successfully and the output was redirected."
    )