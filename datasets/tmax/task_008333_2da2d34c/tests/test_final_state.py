# test_final_state.py

import os
import subprocess
import pytest

def test_sim_cpp_fixed():
    file_path = "/home/user/sim.cpp"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read()

    assert "#pragma omp atomic" not in content, f"{file_path} still contains '#pragma omp atomic'."
    assert "omp parallel" in content, f"{file_path} is missing the OpenMP parallel directive."

def test_sim_compiled():
    exe_path = "/home/user/sim"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_convergence_log():
    log_path = "/home/user/convergence.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    # Compile the agent's code to ensure it's correct and we get the exact expected output
    test_exe = "/tmp/sim_test"
    compile_cmd = ["g++", "-O3", "-fopenmp", "/home/user/sim.cpp", "-o", test_exe]
    subprocess.run(compile_cmd, check=True)

    dt_values = ["0.1", "0.05", "0.025", "0.0125"]
    expected_lines = []

    for dt in dt_values:
        result = subprocess.run([test_exe, dt], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        expected_lines.append(f"{dt},{output}")

    with open(log_path, 'r') as f:
        log_lines = [line.strip() for line in f if line.strip()]

    assert len(log_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(log_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, log_lines)):
        assert actual == expected, f"Line {i+1} in {log_path} is incorrect. Expected '{expected}', got '{actual}'."