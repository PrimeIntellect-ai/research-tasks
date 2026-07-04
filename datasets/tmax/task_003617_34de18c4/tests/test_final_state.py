# test_final_state.py

import os
import subprocess
import json
import pytest

def test_venv_exists():
    """Verify that the virtual environment was created."""
    venv_python = '/home/user/venv/bin/python'
    assert os.path.isfile(venv_python), f"Virtual environment python executable not found at {venv_python}"

    # Check if necessary packages are installed
    result = subprocess.run([venv_python, '-c', 'import h5py, numpy, scipy'], capture_output=True)
    assert result.returncode == 0, "Required libraries (h5py, numpy, scipy) are not installed in the virtual environment."

def get_expected_values():
    """Compute expected values using the user's virtual environment."""
    script = """
import h5py
import numpy as np
from scipy.stats import gaussian_kde
import json

try:
    with h5py.File('/home/user/input_data.h5', 'r') as f:
        mats = f['matrices'][:]

    conds = np.linalg.cond(mats)
    indices = np.where(conds >= 1e12)[0].tolist()

    log_conds = np.log10(conds)
    kde = gaussian_kde(log_conds)
    val = kde(12.0)[0]
    expected_kde = f"{val:.4f}"

    print(json.dumps({'indices': indices, 'kde': expected_kde}))
except Exception as e:
    pass
"""
    venv_python = '/home/user/venv/bin/python'
    if os.path.isfile(venv_python):
        result = subprocess.run([venv_python, '-c', script], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                return data['indices'], data['kde']
            except json.JSONDecodeError:
                pass

    # Fallback to known truth values for seed 42
    return [14, 27, 55, 89], "0.0097"

def test_singular_indices():
    """Verify that singular_indices.txt contains the correct indices."""
    indices_file = '/home/user/singular_indices.txt'
    assert os.path.isfile(indices_file), f"Output file {indices_file} is missing."

    expected_indices, _ = get_expected_values()

    with open(indices_file, 'r') as f:
        lines = f.read().strip().split('\n')

    actual_indices = []
    for line in lines:
        if line.strip():
            try:
                actual_indices.append(int(line.strip()))
            except ValueError:
                pytest.fail(f"Found non-integer value in {indices_file}: '{line.strip()}'")

    assert actual_indices == expected_indices, f"Expected indices {expected_indices}, but got {actual_indices}"

def test_kde_result():
    """Verify that kde_result.txt contains the correct KDE density value."""
    kde_file = '/home/user/kde_result.txt'
    assert os.path.isfile(kde_file), f"Output file {kde_file} is missing."

    _, expected_kde = get_expected_values()

    with open(kde_file, 'r') as f:
        actual_kde = f.read().strip()

    assert actual_kde == expected_kde, f"Expected KDE value '{expected_kde}', but got '{actual_kde}'"