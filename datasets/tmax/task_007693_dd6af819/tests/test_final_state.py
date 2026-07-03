# test_final_state.py
import os
import subprocess
import pytest

VENV_PYTHON = "/home/user/venv/bin/python"
VENV_PYTEST = "/home/user/venv/bin/pytest"
WORKSPACE = "/home/user/workspace"

def test_venv_and_packages():
    assert os.path.exists(VENV_PYTHON), f"Virtual environment Python not found at {VENV_PYTHON}"

    packages = ["numpy", "scipy", "pytest", "jupyter", "nbformat", "papermill"]
    for pkg in packages:
        result = subprocess.run(
            [VENV_PYTHON, "-c", f"import {pkg}"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Package {pkg} is not installed in the virtual environment. Error: {result.stderr}"

def test_workspace_files_exist():
    expected_files = [
        "mc_sim.py",
        "test_sim.py",
        "create_nb.py",
        "experiment.ipynb",
        "output.ipynb",
        "ks_result.txt"
    ]
    for f in expected_files:
        path = os.path.join(WORKSPACE, f)
        assert os.path.exists(path), f"Expected file {path} does not exist"

def test_test_sim_passes():
    test_file = os.path.join(WORKSPACE, "test_sim.py")
    assert os.path.exists(VENV_PYTEST), f"pytest not found at {VENV_PYTEST}"

    result = subprocess.run(
        [VENV_PYTEST, test_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest on {test_file} failed:\n{result.stdout}\n{result.stderr}"

def test_ks_result_content():
    ks_result_path = os.path.join(WORKSPACE, "ks_result.txt")
    assert os.path.exists(ks_result_path), f"{ks_result_path} does not exist"

    with open(ks_result_path, "r") as f:
        actual_content = f.read().strip()

    # Compute the golden value using the venv's python to ensure exact floating-point matching
    compute_script = """
import numpy as np
import scipy.stats as stats

num_steps = 200
num_trials = 25000
seed = 1001

rng = np.random.default_rng(seed)
angles = rng.uniform(0, 2*np.pi, size=(num_trials, num_steps))
x = np.sum(np.cos(angles), axis=1)
y = np.sum(np.sin(angles), axis=1)
distances = np.sqrt(x**2 + y**2)

scale = np.sqrt(num_steps / 2.0)
statistic, pvalue = stats.kstest(distances, 'rayleigh', args=(), kwds={'scale': scale})

print(f"{statistic:.6f},{pvalue:.6f}")
"""
    result = subprocess.run(
        [VENV_PYTHON, "-c", compute_script],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to compute golden value: {result.stderr}"

    expected_content = result.stdout.strip()
    assert actual_content == expected_content, f"Content of ks_result.txt ({actual_content}) does not match expected ({expected_content})"