# test_final_state.py

import os
import pytest

def test_eigen_extracted():
    """Test that Eigen library is extracted to the correct location."""
    eigen_dir = "/home/user/eigen-3.4.0"
    assert os.path.isdir(eigen_dir), f"Directory {eigen_dir} does not exist."
    eigen_dense = os.path.join(eigen_dir, "Eigen", "Dense")
    assert os.path.isfile(eigen_dense), f"Eigen headers not found at {eigen_dense}. Make sure it is extracted correctly."

def test_cpp_code_fixed():
    """Test that the C++ code uses Cholesky decomposition and removes the bug."""
    cpp_file = "/home/user/mcmc_sequence.cpp"
    assert os.path.isfile(cpp_file), f"File {cpp_file} does not exist."

    with open(cpp_file, 'r') as f:
        content = f.read()

    assert "llt" in content.lower() or "LLT" in content, "Cholesky decomposition (LLT) not used in the C++ file."
    assert "covariance * z" not in content, "The buggy direct multiplication by covariance is still present."

def test_executable_exists():
    """Test that the compiled binary exists and is executable."""
    exe_file = "/home/user/mcmc_sequence"
    assert os.path.isfile(exe_file), f"Executable {exe_file} does not exist. Did you compile the code?"
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_posterior_mean():
    """Test that the output CSV contains the correct estimated posterior mean."""
    csv_file = "/home/user/posterior_mean.csv"
    assert os.path.isfile(csv_file), f"File {csv_file} does not exist. Did you run the compiled binary?"

    with open(csv_file, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 3, f"Expected exactly 3 comma-separated values in CSV, got {len(parts)}."

    try:
        vals = [float(p) for p in parts]
    except ValueError:
        pytest.fail(f"CSV contains non-float values: {content}")

    expected = [2.5, -1.0, 3.1]

    for i, (val, exp) in enumerate(zip(vals, expected)):
        assert abs(val - exp) < 0.05, f"Value at index {i} ({val}) is not within 0.05 of expected ({exp}). The sampler may still be diverging."