# test_final_state.py
import os
import re
import pytest

def test_results_log_exists():
    """Verify that results.log was created."""
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"Missing required file: {log_path}"

def test_results_log_content():
    """Verify that results.log contains the correct output for the extracted guesses."""
    log_path = "/home/user/results.log"
    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 4, f"Expected at least 4 lines in results.log, found {len(lines)}"

    # We expect these specific values based on the pcap setup
    expected_lines = [
        r"GUESS:\s*2\.0\s*RESULT:\s*CONVERGED:\s*1",
        r"GUESS:\s*0\.577350269\s*RESULT:\s*FAILED",
        r"GUESS:\s*-0\.5\s*RESULT:\s*CONVERGED:\s*-1",
        r"GUESS:\s*1\.0\s*RESULT:\s*CONVERGED:\s*1"
    ]

    for i, expected_pattern in enumerate(expected_lines):
        assert re.search(expected_pattern, lines[i]), \
            f"Line {i+1} does not match expected pattern '{expected_pattern}'. Got: '{lines[i]}'"

def test_cpp_code_fixed():
    """Verify that the C++ source code has the requested bug fixes."""
    cpp_path = "/home/user/newton_solver.cpp"
    assert os.path.isfile(cpp_path), f"Missing required file: {cpp_path}"

    with open(cpp_path, "r") as f:
        code = f.read()

    # Check for off-by-one fix
    assert "iter <= MAX_ITER" not in code, \
        "The off-by-one bug (iter <= MAX_ITER) was not fixed in the while loop condition."

    # Check for division by zero / derivative check
    # The instructions say: "If the derivative f'(x) is extremely close to 0 (absolute value < 1e-6), the solver must gracefully abort"
    assert "1e-6" in code, \
        "Could not find the threshold '1e-6' used to check the derivative in newton_solver.cpp."