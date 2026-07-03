# test_final_state.py

import subprocess
import requests
import pytest
import os
import json

def get_expected_brightness(sec):
    cmd = [
        "ffmpeg", "-y", "-ss", str(sec), "-i", "/app/broadcast.mp4",
        "-vframes", "1", "-f", "image2pipe", "-vcodec", "rawvideo",
        "-pix_fmt", "gray", "-"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if proc.returncode != 0 or not proc.stdout:
        return None
    data = proc.stdout
    return sum(data) / len(data)

def test_server_running():
    """Test that the Go server is listening and responding on 127.0.0.1:8080."""
    try:
        resp = requests.get("http://127.0.0.1:8080/report", timeout=2)
        assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Could not connect to Go server on 127.0.0.1:8080. Is it running? Error: {e}")

def test_api_data_endpoint():
    """Test the /api/data endpoint for second 2."""
    try:
        resp = requests.get("http://127.0.0.1:8080/api/data?sec=2", timeout=2)
        assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"

        try:
            data = resp.json()
        except json.JSONDecodeError:
            pytest.fail(f"Response from /api/data?sec=2 is not valid JSON. Response text: {resp.text}")

        assert "second" in data, "Missing 'second' key in JSON response"
        assert data["second"] == 2, f"Expected 'second' to be 2, got {data['second']}"

        assert "brightness" in data, "Missing 'brightness' key in JSON response"
        assert isinstance(data["brightness"], (int, float)), "Brightness must be a number"

        assert "payload" in data, "Missing 'payload' key in JSON response"
        assert isinstance(data["payload"], str), "Payload must be a string"

        expected_brightness = get_expected_brightness(2)
        if expected_brightness is not None:
            # Allow a reasonable delta for different grayscale conversion methods
            assert abs(data["brightness"] - expected_brightness) < 5.0, \
                f"Brightness value {data['brightness']} is too far from expected {expected_brightness}"

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to /api/data?sec=2 failed: {e}")

def test_report_endpoint():
    """Test the /report endpoint formatting."""
    try:
        resp = requests.get("http://127.0.0.1:8080/report", timeout=2)
        assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"

        text = resp.text
        assert text.strip(), "Report response is empty"

        # Check that it contains the expected format for at least one line
        lines = [line for line in text.split('\n') if line.strip()]
        assert any(line.startswith("Sec ") for line in lines), "Report does not contain lines starting with 'Sec '"
        assert any("Brightness" in line for line in lines), "Report does not contain 'Brightness'"
        assert any("Payload:" in line for line in lines), "Report does not contain 'Payload:'"

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to /report failed: {e}")