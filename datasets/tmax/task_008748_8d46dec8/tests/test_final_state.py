# test_final_state.py

import os
import re
import pytest

def test_optimal_x_file():
    path = "/home/user/optimal_x.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "3.6429", f"Expected optimal_x.txt to contain exactly '3.6429', but got '{content}'."

def test_energy_calc_c_fixed():
    path = "/home/user/energy_calc.c"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check that reduction is used
    assert "reduction" in content, "The C code does not appear to use an OpenMP reduction clause."

    # Check that atomic is removed or not used for total_energy
    # A simple check is to ensure that `#pragma omp atomic` followed by `total_energy += val;` is gone
    atomic_pattern = re.compile(r'#pragma\s+omp\s+atomic\s*total_energy\s*\+=', re.MULTILINE)
    assert not atomic_pattern.search(content), "The C code still contains the non-deterministic atomic directive for total_energy."

def test_energy_calc_executable():
    path = "/home/user/energy_calc"
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.path.isfile(path) and os.access(path, os.X_OK), f"{path} is not executable."

def test_optimize_py_exists():
    path = "/home/user/optimize.py"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."