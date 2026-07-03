# test_final_state.py

import os
import re

def test_executable_exists():
    exe_path = "/home/user/sim/pde_solver"
    assert os.path.isfile(exe_path), f"Executable {exe_path} was not found. Did you compile the C++ code?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_result_log_exists_and_correct():
    log_path = "/home/user/sim/result.log"
    assert os.path.isfile(log_path), f"Result log {log_path} was not found."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_heat = "Total Heat: 20000000.0"
    expected_det = "Determinant: 189.0"

    assert expected_heat in content, f"Expected '{expected_heat}' in {log_path}, but got:\n{content}"
    assert expected_det in content, f"Expected '{expected_det}' in {log_path}, but got:\n{content}"

def test_cpp_constraints():
    cpp_path = "/home/user/sim/pde_solver.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    # Ensure grid is still a vector of floats
    assert re.search(r"std::vector<float>\s+grid\s*\(", content) or "std::vector<float> grid" in content, \
        "The grid data type must remain std::vector<float>. Do not change it to double."

    # Check that no external libraries like Eigen or lapack are included
    assert "Eigen" not in content, "External library Eigen is not allowed."
    assert "lapack" not in content.lower(), "External library LAPACK is not allowed."