# test_final_state.py

import os
import pytest

def test_setup_script_exists_and_executable():
    script_path = "/home/user/setup_env.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_libchecksum_so_exists():
    so_path = "/home/user/environment/libchecksum.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not compiled or is missing."

def test_test_plan_log_content():
    log_path = "/home/user/test_plan.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    expected_lines = [
        "1. libA.c: -2105151528",
        "2. libB.c: 1111624890",
        "3. libC.c: -967156102",
        "4. libD.c: -908992055",
        "5. libE.c: -1106591039"
    ]

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch in {log_path}. Expected '{expected}', got '{actual}'."