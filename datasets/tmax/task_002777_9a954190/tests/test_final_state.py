# test_final_state.py
import os
import json
import ast

def test_venv_exists():
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), "Virtual environment directory /home/user/venv does not exist."
    python_bin = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable not found at {python_bin}."

def test_vdp_mcmc_updated():
    path = "/home/user/vdp_mcmc.py"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "solve_ivp" in content, "solve_ivp not found in vdp_mcmc.py."
    assert "BDF" in content, "method='BDF' not found in vdp_mcmc.py."

def test_samples_exist():
    path = "/home/user/valid_mu_samples.npy"
    assert os.path.isfile(path), f"{path} does not exist. Did the MCMC script run successfully?"

def test_fit_density_exists():
    path = "/home/user/fit_density.py"
    assert os.path.isfile(path), f"{path} does not exist."

def test_kde_results():
    path = "/home/user/kde_results.json"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{path} is not a valid JSON file."

    assert isinstance(results, list), f"Data in {path} must be a JSON list."
    assert len(results) == 5, f"Expected exactly 5 elements in {path}, got {len(results)}."

    for i, val in enumerate(results):
        assert isinstance(val, (int, float)), f"Element at index {i} is not a number: {val}"
        assert val < 0, f"Log-density values should generally be negative, got {val} at index {i}."