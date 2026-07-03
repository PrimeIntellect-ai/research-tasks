# test_final_state.py

import os
import subprocess
import pytest

def test_sorted_outputs_exists_and_correct():
    output_path = '/home/user/rpn_calc/sorted_outputs.txt'
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "25.00",
        "16.00",
        "12.00",
        "7.00",
        "5.00"
    ]

    assert lines == expected_lines, (
        f"Contents of {output_path} do not match the expected sorted outputs.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {lines}"
    )

def test_makefile_fixed():
    makefile_path = '/home/user/rpn_calc/Makefile'
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert "-lm" in content, "Makefile was not updated to link the math library (-lm)."

def test_rpn_calc_binary_exists():
    binary_path = '/home/user/rpn_calc/rpn_calc'
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_rpn_calc_memory_safety():
    c_file_path = '/home/user/rpn_calc/rpn_calc.c'
    assert os.path.isfile(c_file_path), f"Source file {c_file_path} is missing."

    with open(c_file_path, 'r') as f:
        content = f.read()

    # Check for stderr and exit code 1 logic
    assert "stderr" in content, "rpn_calc.c does not print to stderr upon error."

    # Check if the binary actually catches overflow
    binary_path = '/home/user/rpn_calc/rpn_calc'
    if os.path.isfile(binary_path) and os.access(binary_path, os.X_OK):
        # Run a test that should trigger stack overflow
        overflow_expr = "1 " * 15 + "+ " * 14
        result = subprocess.run([binary_path, overflow_expr], capture_output=True, text=True)
        assert result.returncode == 1, "rpn_calc binary did not exit with code 1 on stack overflow."
        assert "Error" in result.stderr, "rpn_calc binary did not print 'Error' to stderr on stack overflow."

        # Run a test that should trigger stack underflow
        underflow_expr = "3 +"
        result = subprocess.run([binary_path, underflow_expr], capture_output=True, text=True)
        assert result.returncode == 1, "rpn_calc binary did not exit with code 1 on stack underflow."
        assert "Error" in result.stderr, "rpn_calc binary did not print 'Error' to stderr on stack underflow."