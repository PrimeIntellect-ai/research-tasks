# test_final_state.py

import os
import requests
import pytest

def test_output_files_exist_and_are_floats():
    """Test that the required output files exist and contain valid float values."""
    files_to_check = [
        "/home/user/correlation.txt",
        "/home/user/mse.txt",
        "/home/user/benchmark.txt"
    ]

    for file_path in files_to_check:
        assert os.path.exists(file_path), f"Required file missing: {file_path}"
        assert os.path.isfile(file_path), f"Path is not a file: {file_path}"

        with open(file_path, "r") as f:
            content = f.read().strip()

        try:
            float_val = float(content)
        except ValueError:
            pytest.fail(f"File {file_path} does not contain a valid float. Content: '{content}'")

def test_go_code_directory_exists():
    """Test that the Go code directory exists."""
    go_dir = "/home/user/traffic_model/"
    assert os.path.exists(go_dir), f"Go code directory missing: {go_dir}"
    assert os.path.isdir(go_dir), f"Path is not a directory: {go_dir}"

def test_http_server_predict_endpoint():
    """Test the HTTP server endpoint for predictions."""
    url = "http://127.0.0.1:9090/predict?frame_id=5"
    headers = {"Authorization": "Bearer my-secret-token"}

    # Test valid request
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "frame_id" in data, "JSON response missing 'frame_id' key"
    assert data["frame_id"] == 5, f"Expected frame_id=5, got {data['frame_id']}"

    assert "predicted_variance" in data, "JSON response missing 'predicted_variance' key"
    assert isinstance(data["predicted_variance"], (float, int)), f"predicted_variance should be a number, got {type(data['predicted_variance'])}"

def test_http_server_auth_required():
    """Test that the HTTP server requires authorization."""
    url = "http://127.0.0.1:9090/predict?frame_id=5"

    try:
        response = requests.get(url, timeout=5)
        # Should not be 200 OK without auth token
        assert response.status_code != 200, "Server allowed access without Authorization header"
    except requests.exceptions.RequestException:
        # If it drops the connection or fails without auth, that's also acceptable
        pass