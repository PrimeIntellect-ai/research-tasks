# test_final_state.py

import os
import json
import subprocess
import sys
import pytest

def test_notebook_fixed():
    """Check that the notebook has been updated to use dt = 0.01."""
    notebook_path = "/home/user/mcmc_fit.ipynb"
    assert os.path.isfile(notebook_path), f"Notebook file is missing: {notebook_path}"

    with open(notebook_path, 'r') as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Notebook is not a valid JSON file.")

    code_content = ""
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            if isinstance(source, list):
                source = "".join(source)
            code_content += source

    assert "dt = 0.01" in code_content, "The notebook does not contain the corrected 'dt = 0.01' statement."
    assert "dt = 0.5" not in code_content, "The notebook still contains the buggy 'dt = 0.5' statement."

def test_posterior_file_exists_and_valid():
    """Check that posterior.h5 was generated and contains the 'chain' dataset."""
    posterior_path = "/home/user/posterior.h5"
    assert os.path.isfile(posterior_path), f"Posterior file is missing: {posterior_path}. Did you run the notebook?"

    # Use subprocess to check HDF5 structure since h5py is a third-party library
    checker_code = """
import sys
try:
    import h5py
except ImportError:
    print("MISSING_H5PY")
    sys.exit(0)

try:
    with h5py.File('/home/user/posterior.h5', 'r') as f:
        if 'chain' not in f:
            print("NO_CHAIN")
        else:
            shape = f['chain'].shape
            print(f"SHAPE:{shape[0]},{shape[1]}")
except Exception as e:
    print(f"ERROR:{e}")
"""
    result = subprocess.run([sys.executable, "-c", checker_code], capture_output=True, text=True)
    out = result.stdout.strip()

    assert "ERROR" not in out, f"Failed to read posterior.h5. It might be corrupted or not a valid HDF5 file. Details: {out}"
    assert "NO_CHAIN" not in out, "Dataset 'chain' not found in posterior.h5."
    assert "SHAPE:1000,2" in out, f"Dataset 'chain' has an unexpected shape. Expected (1000, 2), got output: {out}"

def test_alpha_mean_correct():
    """Check that alpha_mean.txt contains the correct mean value rounded to 2 decimal places."""
    txt_path = "/home/user/alpha_mean.txt"
    assert os.path.isfile(txt_path), f"alpha_mean.txt is missing: {txt_path}"

    with open(txt_path, 'r') as f:
        student_val = f.read().strip()

    # Compute the expected value dynamically from the generated posterior.h5
    compute_code = """
import h5py
import numpy as np
with h5py.File('/home/user/posterior.h5', 'r') as f:
    chain = f['chain'][:]
mean_alpha = np.mean(chain[100:, 0])
print(f"{mean_alpha:.2f}")
"""
    result = subprocess.run([sys.executable, "-c", compute_code], capture_output=True, text=True)
    expected_val = result.stdout.strip()

    assert expected_val != "", "Failed to compute expected mean from posterior.h5."
    assert student_val == expected_val, f"Incorrect mean value in alpha_mean.txt. Expected '{expected_val}', but got '{student_val}'."