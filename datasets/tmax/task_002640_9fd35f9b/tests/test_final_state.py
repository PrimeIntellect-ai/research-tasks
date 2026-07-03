# test_final_state.py

import os
import subprocess
import pytest

def calc_expected_cost(n, d):
    if d == 0:
        return n * 1.5
    return calc_expected_cost((n * 3) % 17, d - 1) / 2.0 + n

@pytest.fixture
def expected_value():
    return f"{calc_expected_cost(5, 10):.4f}"

def test_solution_file_exists_and_correct(expected_value):
    solution_path = "/home/user/incident_1029/solution.txt"
    assert os.path.isfile(solution_path), f"Solution file {solution_path} does not exist."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    assert content == expected_value, f"Solution file content '{content}' does not match expected '{expected_value}'."

def test_binary_compiles_and_runs(expected_value):
    binary_path = "/home/user/incident_1029/route_optimizer"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."

    try:
        result = subprocess.run(
            [binary_path, "5", "10"],
            cwd="/home/user/incident_1029",
            capture_output=True,
            text=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Running the binary timed out. The infinite recursion bug might not be fixed.")

    assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output == expected_value, f"Binary output '{output}' does not match expected '{expected_value}'."

def test_dynamic_linking():
    binary_path = "/home/user/incident_1029/route_optimizer"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."

    result = subprocess.run(["ldd", binary_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run ldd on the binary."

    # Check if libcustommath.so is resolved
    output = result.stdout
    assert "libcustommath.so => not found" not in output, "libcustommath.so is not correctly linked (missing rpath or library path)."
    assert "libcustommath.so =>" in output, "libcustommath.so does not appear in ldd output."

def test_cost_calc_uses_custom_multiply():
    cost_calc_path = "/home/user/incident_1029/cost_calc.c"
    assert os.path.isfile(cost_calc_path), f"File {cost_calc_path} does not exist."

    with open(cost_calc_path, "r") as f:
        content = f.read()

    assert "custom_multiply" in content, "cost_calc.c must use the 'custom_multiply' function for the base case."