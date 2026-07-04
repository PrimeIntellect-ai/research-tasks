# test_final_state.py

import pytest
import requests
import numpy as np
import json

def test_api_mse():
    np.random.seed(42)
    width, height = 50, 50
    input_data = np.random.rand(height, width).astype(np.float64)

    # Expected kernel
    kernel = np.array([[1.5, 0.0, -1.5],
                       [2.0, 0.0, -2.0],
                       [1.5, 0.0, -1.5]])

    # Compute expected
    expected = np.zeros((height, width), dtype=np.float64)
    for y in range(height):
        for x in range(width):
            sum_val = 0.0
            for ky in range(3):
                for kx in range(3):
                    iy = y + ky - 1
                    ix = x + kx - 1
                    if 0 <= iy < height and 0 <= ix < width:
                        sum_val += input_data[iy, ix] * kernel[ky, kx]
            expected[y, x] = sum_val

    payload = {
        "width": width,
        "height": height,
        "data": input_data.flatten().tolist()
    }

    try:
        resp = requests.post("http://127.0.0.1:8000/process", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"

    try:
        resp_json = resp.json()
    except json.JSONDecodeError:
        pytest.fail("Failed to decode JSON response")

    assert "result" in resp_json, "Response JSON missing 'result' key"

    output_data = np.array(resp_json["result"])
    assert output_data.shape == (width * height,), f"Expected output shape ({width * height},), got {output_data.shape}"

    mse = np.mean((expected.flatten() - output_data) ** 2)
    assert mse < 0.05, f"MSE {mse} is not less than the threshold 0.05"