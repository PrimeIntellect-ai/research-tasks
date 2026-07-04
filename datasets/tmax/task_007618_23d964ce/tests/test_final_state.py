# test_final_state.py

import os
import json
import numpy as np
import pytest

def compute_loss_stable(X, y, theta):
    z = np.dot(X, theta)
    return np.sum(np.logaddexp(0, z) - y * z)

def compute_gradient_stable(X, y, theta):
    z = np.dot(X, theta)
    # stable sigmoid
    preds = np.where(z >= 0, 
                     1 / (1 + np.exp(-z)), 
                     np.exp(z) / (1 + np.exp(z)))
    return np.dot(X.T, (preds - y))

@pytest.fixture(scope="module")
def expected_results():
    X_path = '/home/user/data/X.npy'
    y_path = '/home/user/data/y.npy'

    assert os.path.exists(X_path), f"Missing {X_path}"
    assert os.path.exists(y_path), f"Missing {y_path}"

    X = np.load(X_path)
    y = np.load(y_path)

    np.random.seed(42)
    theta = np.random.randn(X.shape[1])

    lr = 0.001
    max_iters = 10000
    prev_loss = float('inf')

    iters = 0
    final_loss = None
    for i in range(max_iters):
        loss = compute_loss_stable(X, y, theta)
        if abs(prev_loss - loss) < 1e-5:
            final_loss = loss
            break
        prev_loss = loss

        grad = compute_gradient_stable(X, y, theta)
        theta = theta - lr * grad
        iters += 1
        final_loss = loss

    return theta, iters, final_loss

def test_theta_saved_and_correct(expected_results):
    theta_path = '/home/user/theta.npy'
    assert os.path.exists(theta_path), f"File {theta_path} was not created."

    student_theta = np.load(theta_path)
    expected_theta, _, _ = expected_results

    assert student_theta.shape == expected_theta.shape, f"theta.npy shape mismatch. Expected {expected_theta.shape}, got {student_theta.shape}"

    # Allow a small tolerance due to possible minor differences in loop structure
    assert np.allclose(student_theta, expected_theta, atol=1e-3), "The saved theta.npy does not match the expected optimized weights."

def test_metrics_saved_and_correct(expected_results):
    metrics_path = '/home/user/metrics.json'
    assert os.path.exists(metrics_path), f"File {metrics_path} was not created."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} does not contain valid JSON.")

    assert "iterations" in metrics, "metrics.json is missing the 'iterations' key."
    assert "final_loss" in metrics, "metrics.json is missing the 'final_loss' key."

    _, expected_iters, expected_loss = expected_results

    student_iters = metrics["iterations"]
    student_loss = metrics["final_loss"]

    assert isinstance(student_iters, int), "'iterations' in metrics.json must be an integer."
    assert isinstance(student_loss, (float, int)), "'final_loss' in metrics.json must be a float."

    # Allow a difference of up to 2 iterations depending on when the break occurs
    assert abs(student_iters - expected_iters) <= 2, f"Expected around {expected_iters} iterations, but got {student_iters}."

    # Loss should be very close
    assert abs(student_loss - expected_loss) < 1e-2, f"Expected final_loss around {expected_loss}, but got {student_loss}."