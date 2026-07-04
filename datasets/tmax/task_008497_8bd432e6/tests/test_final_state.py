# test_final_state.py
import os
import sys
import subprocess

def get_expected_mode():
    """
    Computes the expected mode using the same libraries available in the environment,
    but invoked via subprocess to keep the test file itself strictly stdlib-only.
    """
    script = """
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from scipy.optimize import minimize

df = pd.read_csv('/home/user/observations.csv')
vals = df[['val_1', 'val_2', 'val_3']].values.flatten()
kde = gaussian_kde(vals)

def neg_kde(x):
    return -kde(x)[0]

res = minimize(neg_kde, x0=np.array([0.0]))
print(f"{res.x[0]:.3f}")
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def test_pipeline_script_exists():
    """Check that the pipeline script was created."""
    path = "/home/user/pipeline.py"
    assert os.path.isfile(path), f"Pipeline script {path} does not exist."

def test_result_file_exists():
    """Check that the result file was created."""
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Result file {path} does not exist."

def test_result_content():
    """Check that the result file contains the correct mode value."""
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Result file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_mode = get_expected_mode()

    assert content == expected_mode, (
        f"Incorrect value in {path}. "
        f"Expected '{expected_mode}', but got '{content}'."
    )