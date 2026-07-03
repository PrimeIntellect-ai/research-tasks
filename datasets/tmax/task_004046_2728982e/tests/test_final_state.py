# test_final_state.py
import pytest
import requests
import json
import h5py
import numpy as np
import os

URL = "http://127.0.0.1:8080/features"
AUTH_HEADER = {"X-Auth": "secret-token-123"}

def get_expected_values():
    h5_path = "/home/user/raw_input.h5"
    assert os.path.isfile(h5_path), f"File {h5_path} not found"

    with h5py.File(h5_path, 'r') as f:
        data = f['/data/batch_1'][:]

    total_sum = np.sum(data)
    scale_factor = 1.0 / total_sum
    preview = data[:3] * scale_factor

    # The bash script uses scale=6 for bc, which truncates.
    # Let's format it exactly as the expected output or allow a small tolerance.
    # The truth says: 0.001980 and [0.000198, 0.000396, 0.000594]
    return round(scale_factor, 6), [round(x, 6) for x in preview]

def test_unauthorized_request():
    """Test that requests without the correct X-Auth header are rejected."""
    try:
        response = requests.get(URL, timeout=2)
        # It should either return 403 or drop the connection silently
        if response.status_code != 403:
            pytest.fail(f"Expected 403 Forbidden or dropped connection, got {response.status_code}")
    except requests.exceptions.ConnectionError:
        # Dropped connection is acceptable
        pass
    except requests.exceptions.ReadTimeout:
        # Timeout could also mean dropped/ignored
        pass

def test_authorized_request():
    """Test that authorized requests return the correct deterministic JSON."""
    try:
        response = requests.get(URL, headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        payload = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "scale_factor" in payload, "Missing 'scale_factor' in JSON response"
    assert "normalized_preview" in payload, "Missing 'normalized_preview' in JSON response"

    expected_scale, expected_preview = get_expected_values()

    # Check scale factor with tolerance due to string formatting
    assert abs(payload["scale_factor"] - expected_scale) < 1e-5, \
        f"Expected scale_factor ~{expected_scale}, got {payload['scale_factor']}"

    preview = payload["normalized_preview"]
    assert len(preview) == 3, f"Expected 3 items in normalized_preview, got {len(preview)}"

    for i in range(3):
        assert abs(preview[i] - expected_preview[i]) < 1e-5, \
            f"Expected preview[{i}] ~{expected_preview[i]}, got {preview[i]}"