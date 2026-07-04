# test_final_state.py

import os
import subprocess
import re

def test_solver_bug_fixed():
    solver_file = "/home/user/optimization_lib/solver.py"
    assert os.path.isfile(solver_file), f"File {solver_file} does not exist."

    with open(solver_file, "r") as f:
        content = f.read()

    assert "x = x + fx / dfx" not in content, "The bug 'x = x + fx / dfx' is still present in solver.py."

    fixed_pattern = re.compile(r"x\s*=\s*x\s*-\s*fx\s*/\s*dfx|x\s*-=\s*fx\s*/\s*dfx")
    assert fixed_pattern.search(content), "The update step in solver.py was not correctly fixed to subtraction."

def test_regression_test_file_exists():
    test_file = "/home/user/optimization_lib/tests/test_regression.py"
    assert os.path.isfile(test_file), f"Regression test file {test_file} is missing."

def test_regression_test_content():
    test_file = "/home/user/optimization_lib/tests/test_regression.py"
    assert os.path.isfile(test_file), f"Regression test file {test_file} is missing."

    with open(test_file, "r") as f:
        content = f.read()

    assert "def test_regression_quadratic" in content, "Function 'test_regression_quadratic' missing in test_regression.py."

    # Check for basic required elements in the test file
    assert "9" in content, "The function f(x) = x^2 - 9 does not seem to be defined."
    assert "5.0" in content or "5" in content, "The initial value x0 = 5.0 does not seem to be used."
    assert "10" in content, "The assertion for iterations < 10 is missing."

def test_pytest_passes():
    """Run pytest on the optimization_lib directory and ensure it passes."""
    target_dir = "/home/user/optimization_lib"
    assert os.path.isdir(target_dir), f"Directory {target_dir} is missing."

    result = subprocess.run(
        ["pytest", target_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"pytest failed. Output:\n{result.stdout}\n{result.stderr}"