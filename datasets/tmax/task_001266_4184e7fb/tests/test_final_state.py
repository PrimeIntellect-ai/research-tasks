# test_final_state.py

import os
import stat
import pytest
import numpy as np

def test_run_sh_exists_and_executable():
    """Test that run.sh exists and is executable."""
    run_sh_path = "/home/user/run.sh"
    assert os.path.isfile(run_sh_path), f"{run_sh_path} does not exist."
    st = os.stat(run_sh_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{run_sh_path} is not executable."

def test_requirements_exists():
    """Test that requirements.txt exists."""
    req_path = "/home/user/requirements.txt"
    assert os.path.isfile(req_path), f"{req_path} does not exist."

def test_outputs_exist():
    """Test that the expected output files exist."""
    expected_files = [
        "/home/user/W_out.npy",
        "/home/user/H_out.npy",
        "/home/user/W_heatmap.png"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Expected output file {f} does not exist."

def test_nmf_output_validity():
    """Test that the output matrices are valid (no NaNs, correct shapes)."""
    W_path = "/home/user/W_out.npy"
    H_path = "/home/user/H_out.npy"

    W = np.load(W_path)
    H = np.load(H_path)

    assert not np.isnan(W).any(), "W_out.npy contains NaNs. Stability fix failed."
    assert not np.isnan(H).any(), "H_out.npy contains NaNs. Stability fix failed."

    assert W.shape == (200, 10), f"Expected W shape (200, 10), got {W.shape}"
    assert H.shape == (10, 200), f"Expected H shape (10, 200), got {H.shape}"

def test_nmf_correctness():
    """Test that the NMF output matches the expected vectorized implementation with epsilon."""
    V_path = "/home/user/kmer_matrix.npy"
    W_path = "/home/user/W_out.npy"
    H_path = "/home/user/H_out.npy"

    V = np.load(V_path)

    # Compute expected W and H
    n, m = V.shape
    k = 10
    iters = 50
    eps = 1e-9

    np.random.seed(42)
    W_expected = np.random.rand(n, k)
    H_expected = np.random.rand(k, m)

    for _ in range(iters):
        # Update H
        num_H = W_expected.T @ V
        den_H = W_expected.T @ (W_expected @ H_expected)
        H_expected = H_expected * (num_H / (den_H + eps))

        # Update W
        num_W = V @ H_expected.T
        den_W = (W_expected @ H_expected) @ H_expected.T
        W_expected = W_expected * (num_W / (den_W + eps))

    W_actual = np.load(W_path)
    H_actual = np.load(H_path)

    np.testing.assert_allclose(
        W_actual, W_expected, rtol=1e-5, atol=1e-8,
        err_msg="W_out.npy does not match expected values. Ensure epsilon=1e-9 is added to the denominator and operations are correctly vectorized."
    )

    np.testing.assert_allclose(
        H_actual, H_expected, rtol=1e-5, atol=1e-8,
        err_msg="H_out.npy does not match expected values. Ensure epsilon=1e-9 is added to the denominator and operations are correctly vectorized."
    )