# test_final_state.py

import os
import tempfile
import pytest
import requests
import numpy as np
import h5py
from scipy.stats import kstest

def test_svd_endpoint():
    """
    Validates that the server at 127.0.0.1:8080 correctly processes an HDF5 payload,
    computes SVD, performs a KS test against uniform(0,1), and returns the correct JSON.
    """
    url = "http://127.0.0.1:8080/test_svd"

    # Generate a test matrix with known singular values
    # We use a diagonal matrix so the singular values are exactly the absolute values of the diagonal elements
    matrix = np.diag([0.1, 0.5, 0.9])

    # Compute expected results
    singular_values = [0.1, 0.5, 0.9]
    expected_p_value = kstest(singular_values, 'uniform').pvalue
    expected_reject = expected_p_value < 0.05

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        tmp_name = tmp.name

    try:
        with h5py.File(tmp_name, 'w') as f:
            f.create_dataset('matrix', data=matrix)

        with open(tmp_name, 'rb') as f:
            payload = f.read()

        try:
            resp = requests.post(url, data=payload, timeout=5)
        except requests.exceptions.ConnectionError:
            pytest.fail(f"Could not connect to {url}. Is the server running?")

        assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}. Response: {resp.text}"

        try:
            data = resp.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON. Response text: {resp.text}")

        assert "p_value" in data, "Response JSON is missing 'p_value' key."
        assert "reject" in data, "Response JSON is missing 'reject' key."

        assert isinstance(data["p_value"], (int, float)), "'p_value' must be a float."
        assert isinstance(data["reject"], bool), "'reject' must be a boolean."

        assert abs(data["p_value"] - expected_p_value) < 1e-4, \
            f"Expected p_value ~ {expected_p_value:.5f}, got {data['p_value']}"
        assert data["reject"] == expected_reject, \
            f"Expected reject={expected_reject}, got {data['reject']}"

    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)