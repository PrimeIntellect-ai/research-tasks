# test_final_state.py
import os
import pandas as pd
import numpy as np

def test_long_signals_format():
    path = "/home/user/long_signals.csv"
    assert os.path.isfile(path), f"Reshaped data file missing: {path}"

    # Check headers
    df = pd.read_csv(path, nrows=5)
    expected_cols = ["Time", "NodeID", "Value"]
    assert list(df.columns) == expected_cols, f"Incorrect headers in {path}. Expected {expected_cols}, got {list(df.columns)}"

def test_final_densities_mse():
    pred_path = "/home/user/final_densities.txt"
    ref_path = "/app/reference_densities.txt"

    assert os.path.isfile(pred_path), f"Final output missing: {pred_path}"
    assert os.path.isfile(ref_path), f"Reference output missing: {ref_path}"

    # Read the density values (assuming format: NodeID, Density)
    pred_df = pd.read_csv(pred_path, header=None)
    ref_df = pd.read_csv(ref_path, header=None)

    assert pred_df.shape[1] >= 2, f"Expected at least 2 columns in {pred_path}"

    pred = pred_df.values[:, 1].astype(float)
    ref = ref_df.values[:, 1].astype(float)

    assert len(pred) == len(ref), f"Length mismatch: pred={len(pred)}, ref={len(ref)}"

    mse = np.mean((pred - ref)**2)
    threshold = 1e-6

    assert mse <= threshold, f"MSE {mse} exceeds the threshold of {threshold}. The spectral density calculation is incorrect."

def test_makefile_fixed():
    path = "/app/libspectral-0.1/Makefile"
    assert os.path.isfile(path), f"Makefile missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "-fopenmp" in content, "Makefile does not contain OpenMP flags (-fopenmp)"

def test_c_file_fixed():
    path = "/app/libspectral-0.1/src/spectral_density.c"
    assert os.path.isfile(path), f"C source file missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "omp parallel for" in content, "OpenMP pragma (#pragma omp parallel for) missing in C file"
    assert "sqrt(re + im)" not in content.replace(" ", ""), "Mathematical bug (sqrt(re + im)) is still present in the C file"