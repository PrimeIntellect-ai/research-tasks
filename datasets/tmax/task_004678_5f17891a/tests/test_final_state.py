# test_final_state.py
import os
import math
import subprocess

def test_density_sim_c_modified():
    c_file = "/home/user/density_sim.c"
    assert os.path.exists(c_file), f"File {c_file} does not exist."

    with open(c_file, 'r') as f:
        content = f.read()

    assert "#pragma omp atomic" not in content, "The file density_sim.c still contains '#pragma omp atomic'."
    assert "compute_node_weight" in content, "The function 'compute_node_weight' is missing from density_sim.c."

def test_executable_exists():
    exe_file = "/home/user/density_sim"
    assert os.path.exists(exe_file), f"Executable {exe_file} does not exist. Did you compile it?"
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_output_file_and_value():
    out_file = "/home/user/reproducible_density.txt"
    assert os.path.exists(out_file), f"Output file {out_file} does not exist."

    with open(out_file, 'r') as f:
        content = f.read().strip()

    assert content, f"File {out_file} is empty."

    try:
        actual_val = float(content)
    except ValueError:
        assert False, f"Content of {out_file} is not a valid float: {content}"

    # Compute the expected value
    expected_val = 0.0
    for i in range(100000):
        expected_val += math.sin(i)**2 + math.cos(i / 2.0)

    # The expected value is approximately 50000.3207080170
    # We check if it's extremely close to the expected sequential sum
    assert math.isclose(actual_val, expected_val, rel_tol=1e-10), f"Calculated density {actual_val} does not match expected sequential sum {expected_val}."