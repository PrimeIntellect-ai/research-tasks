# test_final_state.py

import os
import pytest

def test_setup_py_fixed():
    setup_path = "/home/user/pde_solver/setup.py"
    assert os.path.isfile(setup_path), f"{setup_path} is missing"
    with open(setup_path, "r") as f:
        content = f.read()
    assert "get_include" in content, "setup.py was not fixed to include numpy.get_include()"

def test_solver_pyx_fixed():
    solver_path = "/home/user/pde_solver/solver.pyx"
    assert os.path.isfile(solver_path), f"{solver_path} is missing"
    with open(solver_path, "r") as f:
        content = f.read()
    assert "range(1, N-1)" in content.replace(" ", ""), "solver.pyx was not fixed to correct the boundary condition (range(1, N-1))"

def test_mre_output_correct():
    output_path = "/home/user/pde_solver/mre_output.txt"
    assert os.path.isfile(output_path), f"{output_path} is missing. Did you create mre.py and write the output?"
    with open(output_path, "r") as f:
        content = f.read().strip()

    # Expected math logic after 2 steps:
    # Initial: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    # Step 1: [0, 0, 0, 0, 0.1, 0.8, 0.1, 0, 0, 0]
    # Step 2: [0.0, 0.0, 0.0, 0.01, 0.16, 0.66, 0.16, 0.01, 0.0, 0.0]

    expected_values = [0.0, 0.0, 0.0, 0.01, 0.16, 0.66, 0.16, 0.01, 0.0, 0.0]

    actual_values_str = content.split(",")
    assert len(actual_values_str) == 10, f"Expected 10 values in mre_output.txt, but got {len(actual_values_str)}"

    for i, (actual_str, expected) in enumerate(zip(actual_values_str, expected_values)):
        try:
            actual = float(actual_str)
        except ValueError:
            pytest.fail(f"Value at index {i} in mre_output.txt is not a valid float: {actual_str}")

        assert abs(actual - expected) < 1e-7, f"Value at index {i} is incorrect. Expected {expected}, got {actual}"