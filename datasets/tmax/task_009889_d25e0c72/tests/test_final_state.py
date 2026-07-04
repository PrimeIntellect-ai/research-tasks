# test_final_state.py

import os
import json
import subprocess
import pytest

WORKSPACE = "/home/user/model_fitting"

def test_integrator_test_passes():
    """Check that the provided test_integrator.py passes successfully."""
    test_file = os.path.join(WORKSPACE, "test_integrator.py")
    assert os.path.isfile(test_file), f"Test file {test_file} is missing."

    result = subprocess.run(
        ["pytest", test_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest on {test_file} failed. Output:\n{result.stdout}\n{result.stderr}"

def test_posterior_samples_exist_and_shape():
    """Check that posterior_samples.npy exists and has the correct shape."""
    samples_file = os.path.join(WORKSPACE, "posterior_samples.npy")
    assert os.path.isfile(samples_file), f"File {samples_file} is missing. MCMC script may not have saved it."

    # Use numpy to load and check shape if available, but since we can only use stdlib,
    # we can't import numpy directly in the test unless we assume it's installed.
    # The prompt says "Use only the Python standard library and pytest (no third-party libs)".
    # However, the environment has numpy installed (as per the task). 
    # To be strictly compliant with "no third-party libs" for the test script itself, 
    # we can run a short python snippet via subprocess.

    check_script = f"""
import numpy as np
import sys
try:
    data = np.load('{samples_file}')
    if data.shape != (5000, 2):
        print(f"Wrong shape: {{data.shape}}")
        sys.exit(1)
except Exception as e:
    print(str(e))
    sys.exit(1)
"""
    result = subprocess.run(["python3", "-c", check_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to load or verify shape of posterior_samples.npy: {result.stdout.strip()}"

def test_map_estimate_json():
    """Check that map_estimate.json exists and has valid parameters."""
    json_file = os.path.join(WORKSPACE, "map_estimate.json")
    assert os.path.isfile(json_file), f"File {json_file} is missing."

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_file} is not valid JSON.")

    assert "omega" in data, "Key 'omega' missing in map_estimate.json"
    assert "gamma" in data, "Key 'gamma' missing in map_estimate.json"

    omega = data["omega"]
    gamma = data["gamma"]

    # Check that they are numbers
    assert isinstance(omega, (int, float)), "omega must be a number"
    assert isinstance(gamma, (int, float)), "gamma must be a number"

    # Check approximate values (omega ~ 2.0, gamma ~ 0.1)
    # Allow some tolerance due to MCMC randomness
    assert 1.0 < omega < 3.0, f"omega value {omega} is too far from expected ~2.0"
    assert 0.0 < gamma < 0.5, f"gamma value {gamma} is too far from expected ~0.1"

def test_fit_plot_generated():
    """Check that the visualization plot was generated."""
    plot_file = os.path.join(WORKSPACE, "fit_plot.png")
    assert os.path.isfile(plot_file), f"File {plot_file} is missing. Visualization script may not have run."
    assert os.path.getsize(plot_file) > 0, f"File {plot_file} is empty."