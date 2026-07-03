# test_final_state.py

import os
import re
import pytest

def test_mcmc_mapper_cpp_exists():
    file_path = "/home/user/mcmc_mapper.cpp"
    assert os.path.exists(file_path), f"The source file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a regular file."

def test_mcmc_mapper_executable_exists():
    file_path = "/home/user/mcmc_mapper"
    assert os.path.exists(file_path), f"The executable {file_path} is missing. Did you compile the code?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a regular file."
    assert os.access(file_path, os.X_OK), f"The file {file_path} is not executable."

def test_mesh_stats_output():
    file_path = "/home/user/mesh_stats.txt"
    assert os.path.exists(file_path), f"The output file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "Final bins: 11", f"Expected 'Final bins: 11' in {file_path}, but got '{content}'."

def test_posterior_mean_output():
    file_path = "/home/user/posterior_mean.txt"
    assert os.path.exists(file_path), f"The output file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    match = re.match(r"^Mean mu:\s*([0-9.]+)$", content)
    assert match is not None, f"The format of {file_path} is incorrect. Expected 'Mean mu: <value>', got '{content}'."

    mean_val = float(match.group(1))

    # Allow some tolerance for MCMC variance and rounding
    assert 42.30 <= mean_val <= 42.55, f"Expected posterior mean to be around 42.42, but got {mean_val}."