# test_final_state.py

import os
import json
import socket
import requests
import pytest

MSE_RESULTS_PATH = "/home/user/mse_results.json"
PLOT_IMAGE_PATH = "/home/user/motion_plot.png"

def test_mse_results_exist_and_valid():
    assert os.path.exists(MSE_RESULTS_PATH), f"File {MSE_RESULTS_PATH} does not exist."
    with open(MSE_RESULTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{MSE_RESULTS_PATH} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected a list in {MSE_RESULTS_PATH}."
    assert len(data) > 0, f"List in {MSE_RESULTS_PATH} is empty."
    assert all(isinstance(x, (int, float)) for x in data), f"List in {MSE_RESULTS_PATH} must contain floats."

def test_plot_image_exists_and_valid():
    assert os.path.exists(PLOT_IMAGE_PATH), f"File {PLOT_IMAGE_PATH} does not exist."
    size = os.path.getsize(PLOT_IMAGE_PATH)
    assert size > 1000, f"File {PLOT_IMAGE_PATH} seems too small to be a valid plot (size: {size} bytes)."

    with open(PLOT_IMAGE_PATH, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", f"File {PLOT_IMAGE_PATH} is not a valid PNG image."

def test_http_service():
    with open(MSE_RESULTS_PATH, "r") as f:
        data = json.load(f)

    max_val = max(data)
    max_idx = data.index(max_val) + 1  # 1-indexed for frame i

    try:
        response = requests.get("http://127.0.0.1:8080/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP GET to /stats failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    try:
        resp_json = response.json()
    except json.JSONDecodeError:
        pytest.fail("HTTP response body is not valid JSON.")

    assert "max_mse_frame" in resp_json, "Missing 'max_mse_frame' in HTTP response."
    assert "max_mse_value" in resp_json, "Missing 'max_mse_value' in HTTP response."

    assert resp_json["max_mse_frame"] == max_idx, f"Expected max_mse_frame to be {max_idx}, got {resp_json['max_mse_frame']}"
    # Allow small floating point differences
    assert abs(resp_json["max_mse_value"] - max_val) < 1e-4, f"Expected max_mse_value to be {max_val}, got {resp_json['max_mse_value']}"

def test_tcp_service():
    with open(PLOT_IMAGE_PATH, "rb") as f:
        expected_data = f.read()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("127.0.0.1", 9090))
        s.sendall(b"PLOT\n")

        received_data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            received_data += chunk

        s.close()
    except Exception as e:
        pytest.fail(f"TCP connection or data transfer failed: {e}")

    assert received_data == expected_data, "Data received from TCP service does not match the contents of motion_plot.png."
    assert received_data.startswith(b"\x89PNG\r\n\x1a\n"), "Received data is not a valid PNG."