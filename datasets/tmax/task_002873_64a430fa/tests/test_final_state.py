# test_final_state.py
import math
import subprocess
import requests

def test_metrics_endpoint():
    # 1. Calculate expected values
    audio_path = "/app/dataset.wav"
    cmd = [
        "ffprobe", "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        audio_path
    ]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
        expected_duration = float(output)
    except Exception as e:
        raise RuntimeError(f"Failed to extract duration from {audio_path}: {e}")

    expected_z = (expected_duration - 10.0) / 2.0
    expected_post_mean = (2.5 + expected_duration) / 1.25

    # 2. Query the service
    try:
        resp = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
    except requests.RequestException as e:
        raise AssertionError(f"Failed to connect to the Go server on 127.0.0.1:8080: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        raise AssertionError(f"Response is not valid JSON. Response: {resp.text}")

    # 3. Verify the JSON structure and values
    assert "duration" in data, "Missing 'duration' in JSON response"
    assert "z_score" in data, "Missing 'z_score' in JSON response"
    assert "posterior_mean" in data, "Missing 'posterior_mean' in JSON response"

    assert math.isclose(data["duration"], expected_duration, rel_tol=1e-3), \
        f"Expected duration approx {expected_duration}, got {data['duration']}"

    assert math.isclose(data["z_score"], expected_z, rel_tol=1e-3), \
        f"Expected z_score approx {expected_z}, got {data['z_score']}"

    assert math.isclose(data["posterior_mean"], expected_post_mean, rel_tol=1e-3), \
        f"Expected posterior_mean approx {expected_post_mean}, got {data['posterior_mean']}"