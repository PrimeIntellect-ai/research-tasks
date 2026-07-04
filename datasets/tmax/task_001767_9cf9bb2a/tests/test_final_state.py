# test_final_state.py

import os
import numpy as np
import pytest

def test_package_installed():
    """Verify that the vendored package was successfully installed and is importable."""
    try:
        import bayes_metrics_tracker
    except ImportError as e:
        pytest.fail(f"Failed to import bayes_metrics_tracker. The package was not installed correctly. Error: {e}")

def test_artifact_exists():
    """Verify that the expected artifact file was generated."""
    artifact_path = "/home/user/artifacts/best_cov_matrix.npy"
    assert os.path.isfile(artifact_path), f"Expected artifact file not found at {artifact_path}"

def test_covariance_matrix_mse():
    """Verify that the estimated covariance matrix meets the MSE threshold."""
    artifact_path = "/home/user/artifacts/best_cov_matrix.npy"
    reference_path = "/app/reference/true_cov_matrix.npy"

    assert os.path.isfile(artifact_path), f"Artifact file {artifact_path} is missing."
    assert os.path.isfile(reference_path), f"Reference file {reference_path} is missing."

    try:
        pred_cov = np.load(artifact_path)
    except Exception as e:
        pytest.fail(f"Failed to load the predicted covariance matrix from {artifact_path}. Error: {e}")

    try:
        true_cov = np.load(reference_path)
    except Exception as e:
        pytest.fail(f"Failed to load the reference covariance matrix from {reference_path}. Error: {e}")

    assert pred_cov.shape == true_cov.shape, (
        f"Shape mismatch: Predicted shape {pred_cov.shape} != Reference shape {true_cov.shape}"
    )

    mse = np.mean((pred_cov - true_cov) ** 2)
    threshold = 0.02

    assert mse < threshold, (
        f"Mean Squared Error (MSE) is too high. "
        f"Expected strictly less than {threshold}, but got {mse:.4f}."
    )