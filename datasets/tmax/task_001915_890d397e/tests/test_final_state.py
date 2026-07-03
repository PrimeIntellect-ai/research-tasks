# test_final_state.py
import os
import json
import math
import subprocess
import pytest

def test_virtual_environment_exists():
    venv_path = '/home/user/venv'
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} does not exist."

    python_bin = os.path.join(venv_path, 'bin', 'python')
    assert os.path.isfile(python_bin) or os.path.isfile(os.path.join(venv_path, 'Scripts', 'python.exe')), \
        "Python executable not found in the virtual environment."

def test_required_packages_installed():
    venv_python = '/home/user/venv/bin/python'
    if not os.path.exists(venv_python):
        venv_python = '/home/user/venv/Scripts/python.exe'

    assert os.path.exists(venv_python), "Cannot find venv python executable to check packages."

    packages = ['numpy', 'scipy', 'matplotlib', 'pandas']
    for pkg in packages:
        result = subprocess.run([venv_python, '-c', f'import {pkg}'], capture_output=True)
        assert result.returncode == 0, f"Package '{pkg}' is not installed in the virtual environment or fails to import."

def test_metrics_json_correct():
    metrics_path = '/home/user/artifacts/metrics.json'
    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} does not exist."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} is not a valid JSON file.")

    expected_keys = {"posterior_alpha", "posterior_beta", "posterior_mean", "posterior_variance"}
    assert set(metrics.keys()) == expected_keys, f"Metrics JSON must contain exactly keys {expected_keys}. Found: {list(metrics.keys())}"

    # Calculate expected values based on setup
    successes = 3450
    trials = 10000
    expected_alpha = 1 + successes
    expected_beta = 1 + (trials - successes)
    expected_mean = expected_alpha / (expected_alpha + expected_beta)
    expected_variance = (expected_alpha * expected_beta) / (((expected_alpha + expected_beta) ** 2) * (expected_alpha + expected_beta + 1))

    assert isinstance(metrics["posterior_alpha"], int), "posterior_alpha must be an integer."
    assert isinstance(metrics["posterior_beta"], int), "posterior_beta must be an integer."
    assert isinstance(metrics["posterior_mean"], float), "posterior_mean must be a float."
    assert isinstance(metrics["posterior_variance"], float), "posterior_variance must be a float."

    assert metrics["posterior_alpha"] == expected_alpha, f"Expected posterior_alpha={expected_alpha}, got {metrics['posterior_alpha']}"
    assert metrics["posterior_beta"] == expected_beta, f"Expected posterior_beta={expected_beta}, got {metrics['posterior_beta']}"

    assert math.isclose(metrics["posterior_mean"], expected_mean, rel_tol=1e-5), \
        f"Expected posterior_mean ~ {expected_mean}, got {metrics['posterior_mean']}"
    assert math.isclose(metrics["posterior_variance"], expected_variance, rel_tol=1e-5), \
        f"Expected posterior_variance ~ {expected_variance}, got {metrics['posterior_variance']}"

def test_posterior_plot_exists_and_valid():
    plot_path = '/home/user/artifacts/posterior.png'
    assert os.path.isfile(plot_path), f"Plot file {plot_path} does not exist."

    size = os.path.getsize(plot_path)
    assert size > 2000, f"Plot file {plot_path} is too small ({size} bytes). It is likely empty or blank."

    with open(plot_path, 'rb') as f:
        header = f.read(8)
        # PNG magic number: \x89PNG\r\n\x1a\n
        assert header == b'\x89PNG\r\n\x1a\n', f"File {plot_path} is not a valid PNG image."