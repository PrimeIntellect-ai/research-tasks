# test_final_state.py

import os
import time
import requests
import pytest

def test_spectral_extractor_compiled():
    """Check that the C++ utility is compiled and placed at the correct location."""
    binary_path = "/app/bin/spectral_extractor"
    assert os.path.exists(binary_path), f"Compiled binary missing at {binary_path}"
    assert os.path.isfile(binary_path), f"{binary_path} is not a file"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_server_ready_file():
    """Check that the server_ready.txt file is created with the correct content."""
    ready_file = "/app/server_ready.txt"
    assert os.path.exists(ready_file), f"Ready file missing at {ready_file}"
    with open(ready_file, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"Expected 'READY' in {ready_file}, got '{content}'"

def test_http_unauthorized():
    """Check that the server returns 401 for missing or invalid token."""
    url = "http://127.0.0.1:9090/component/0"

    # Missing token
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")
    assert response.status_code == 401, f"Expected 401 for missing token, got {response.status_code}"

    # Invalid token
    headers = {"Authorization": "Bearer wrongtoken"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")
    assert response.status_code == 401, f"Expected 401 for invalid token, got {response.status_code}"

def test_http_authorized_and_format():
    """Check that the server returns 200 and the correct JSON structure for a valid request."""
    url = "http://127.0.0.1:9090/component/0"
    headers = {"Authorization": "Bearer SecretMLToken2024"}

    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert response.status_code == 200, f"Expected 200 for valid token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "window" in data, "JSON response missing 'window' key"
    assert "features" in data, "JSON response missing 'features' key"

    assert data["window"] == 0, f"Expected window 0, got {data['window']}"

    features = data["features"]
    assert isinstance(features, list), "Features must be a list"
    assert len(features) == 3, f"Expected exactly 3 features for k=3 components, got {len(features)}"

    for f in features:
        assert isinstance(f, (int, float)), f"Feature value {f} is not a number"