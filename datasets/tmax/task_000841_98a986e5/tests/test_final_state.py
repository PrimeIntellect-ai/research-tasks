# test_final_state.py

import os
import math
import random
import requests
import pytest

def test_files_exist():
    h5_path = "/home/user/training_data.h5"
    pkl_path = "/home/user/surrogate.pkl"

    assert os.path.exists(h5_path), f"Training data file {h5_path} does not exist."
    assert os.path.isfile(h5_path), f"{h5_path} is not a file."
    assert os.path.getsize(h5_path) > 0, f"{h5_path} is empty."

    assert os.path.exists(pkl_path), f"Model file {pkl_path} does not exist."
    assert os.path.isfile(pkl_path), f"{pkl_path} is not a file."
    assert os.path.getsize(pkl_path) > 0, f"{pkl_path} is empty."

def test_hdf5_contents():
    try:
        import h5py
    except ImportError:
        pytest.fail("h5py is not installed, cannot verify HDF5 contents.")

    h5_path = "/home/user/training_data.h5"
    try:
        with h5py.File(h5_path, 'r') as f:
            assert 'X' in f, "Dataset 'X' not found in HDF5 file."
            assert 'y' in f, "Dataset 'y' not found in HDF5 file."

            X_shape = f['X'].shape
            y_shape = f['y'].shape

            assert X_shape == (2000, 3), f"Expected X shape (2000, 3), got {X_shape}"
            assert y_shape == (2000,) or y_shape == (2000, 1), f"Expected y shape (2000,), got {y_shape}"
    except Exception as e:
        pytest.fail(f"Failed to read HDF5 file: {e}")

def true_function(x, y, z):
    return math.sin(x) * (y * y) + math.log(abs(z) + 1.0)

def test_web_service_predictions():
    url = "http://127.0.0.1:8000/predict"

    # Generate 10 random test cases
    random.seed(42)
    for _ in range(10):
        x = random.uniform(0.0, 5.0)
        y = random.uniform(0.0, 5.0)
        z = random.uniform(0.0, 5.0)

        payload = {"x": x, "y": y, "z": z}

        try:
            response = requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the web service at {url}: {e}")

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "prediction" in data, f"Response JSON missing 'prediction' key: {data}"

        pred = data["prediction"]
        assert isinstance(pred, (int, float)), f"Prediction must be a number, got {type(pred)}"

        expected = true_function(x, y, z)

        abs_err = abs(pred - expected)
        rel_err = abs_err / max(abs(expected), 1e-9)

        assert abs_err < 0.25 or rel_err < 0.05, (
            f"Prediction {pred} for input {payload} is too far from expected {expected}. "
            f"Absolute error: {abs_err}, Relative error: {rel_err}"
        )