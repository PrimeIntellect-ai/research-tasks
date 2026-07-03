# test_final_state.py
import pytest
import requests
import subprocess
import hashlib

def get_hash_for_timestamp(t):
    cmd = [
        "ffmpeg", "-y", "-ss", f"00:00:0{t}", "-i", "/app/video.mp4",
        "-frames:v", "1", "-s", "64x64", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, f"ffmpeg failed for t={t}: {result.stderr.decode()}"
    return hashlib.sha256(result.stdout).hexdigest()

def test_data_endpoint():
    try:
        response = requests.get("http://127.0.0.1:9000/data", timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at http://127.0.0.1:9000/data: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(data, list), f"Response JSON must be a list of objects, got {type(data)}."
    assert len(data) == 2, f"Expected exactly 2 items in the response (t=1 and t=4 after deduplication and cleaning), got {len(data)}. Data: {data}"

    expected_hash_1 = get_hash_for_timestamp(1)
    expected_hash_4 = get_hash_for_timestamp(4)

    expected_data = [
        {
            "timestamp": 1,
            "frame_hash": expected_hash_1,
            "telemetry_value": 100
        },
        {
            "timestamp": 4,
            "frame_hash": expected_hash_4,
            "telemetry_value": 150
        }
    ]

    assert data == expected_data, f"Response JSON does not match expected output.\nExpected: {expected_data}\nActual: {data}"