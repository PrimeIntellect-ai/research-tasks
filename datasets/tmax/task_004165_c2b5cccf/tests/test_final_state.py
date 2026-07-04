# test_final_state.py

import os
import subprocess
import json
import requests
import pytest

def get_expected_checksum(time_sec):
    cmd = [
        "ffmpeg", "-y", "-ss", str(time_sec), "-i", "/app/drone_footage.mp4",
        "-vframes", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        raw_bytes = result.stdout
        return sum(raw_bytes) % 256
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to extract frame with ffmpeg: {e.stderr.decode()}")

def test_frame_analyzer_compiled():
    path = "/home/user/analyzer/frame_analyzer"
    assert os.path.isfile(path), f"Missing compiled executable: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_api_unauthorized_missing_header():
    url = "http://127.0.0.1:9090/api/v1/analyze?time=2"
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API server: {e}")

def test_api_unauthorized_invalid_header():
    url = "http://127.0.0.1:9090/api/v1/analyze?time=2"
    headers = {"Authorization": "Bearer wrong-key"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API server: {e}")

def test_api_authorized_time_2():
    url = "http://127.0.0.1:9090/api/v1/analyze?time=2"
    headers = {"Authorization": "Bearer test-api-key-88"}
    expected_checksum = get_expected_checksum("2")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type: application/json"

        data = response.json()
        assert "time" in data, "Missing 'time' in JSON response"
        assert str(data["time"]) == "2", f"Expected time '2', got {data['time']}"
        assert "checksum" in data, "Missing 'checksum' in JSON response"
        assert int(data["checksum"]) == expected_checksum, f"Expected checksum {expected_checksum}, got {data['checksum']}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API server: {e}")
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON response. Raw response: {response.text}")

def test_api_authorized_time_5():
    url = "http://127.0.0.1:9090/api/v1/analyze?time=5"
    headers = {"Authorization": "Bearer test-api-key-88"}
    expected_checksum = get_expected_checksum("5")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        data = response.json()
        assert str(data["time"]) == "5", f"Expected time '5', got {data['time']}"
        assert int(data["checksum"]) == expected_checksum, f"Expected checksum {expected_checksum}, got {data['checksum']}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API server: {e}")
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON response. Raw response: {response.text}")