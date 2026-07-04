# test_final_state.py
import os
import requests
import pytest

def test_source_and_binary_exist():
    assert os.path.isfile("/home/user/metric_server.c"), "C source code /home/user/metric_server.c is missing"
    assert os.path.isfile("/home/user/server"), "Compiled binary /home/user/server is missing"
    assert os.access("/home/user/server", os.X_OK), "Compiled binary is not executable"

def test_http_server_response():
    url = "http://127.0.0.1:8080/metrics"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type: application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Body: {response.text}")

    assert "correlation" in data, "Missing 'correlation' in JSON response"
    assert "posterior" in data, "Missing 'posterior' in JSON response"
    assert "file_size" in data, "Missing 'file_size' in JSON response"

    assert abs(data["correlation"] - (-0.9956)) < 0.0001, f"Expected correlation approx -0.9956, got {data['correlation']}"
    assert abs(data["posterior"] - 0.8000) < 0.0001, f"Expected posterior approx 0.8000, got {data['posterior']}"
    assert data["file_size"] == 1500000, f"Expected file_size 1500000, got {data['file_size']}"

    text = response.text.strip()
    assert "-0.9956" in text, "Correlation value not formatted to exactly 4 decimal places in response text"
    assert "0.8000" in text, "Posterior value not formatted to exactly 4 decimal places in response text"