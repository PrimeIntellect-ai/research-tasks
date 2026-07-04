# test_final_state.py

import os
import pickle
import numpy as np
import pytest

def test_model_mse():
    model_path = '/home/user/model.pkl'
    assert os.path.exists(model_path), f"Model file not found at {model_path}"

    # Generate test set
    np.random.seed(999)
    n_samples = 500
    X_test = np.random.randn(n_samples, 10)
    y_test = 3.0 * X_test[:, 1] - 1.5 * X_test[:, 3] + 2.0 * X_test[:, 4] + 0.8 * X_test[:, 7] + np.random.randn(n_samples) * 0.5

    # Extract features used in training (f2, f4, f5, f8)
    X_test_filtered = X_test[:, [1, 3, 4, 7]]

    # Scale test features using sample statistics
    X_test_scaled = (X_test_filtered - np.mean(X_test_filtered, axis=0)) / np.std(X_test_filtered, axis=0)

    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        pytest.fail(f"Failed to load the model pickle file: {e}")

    try:
        preds = model.predict(X_test_scaled)
    except Exception as e:
        pytest.fail(f"Failed to predict using the loaded model: {e}")

    mse = np.mean((y_test - preds)**2)

    assert mse <= 2.5, f"MSE {mse:.4f} is greater than the threshold of 2.5"

def test_engineered_data_exists():
    data_path = '/home/user/engineered.csv'
    assert os.path.exists(data_path), f"Engineered dataset not found at {data_path}"