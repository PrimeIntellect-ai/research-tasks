# test_final_state.py
import os
import wave
import struct
import math
import requests
import pytest

def compute_expected_rms(file_path, window_ms):
    with wave.open(file_path, 'rb') as wf:
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        nframes = wf.getnframes()

        assert nchannels == 1, "Expected mono audio"
        assert sampwidth == 2, "Expected 16-bit PCM"

        raw_data = wf.readframes(nframes)

    samples = struct.unpack(f"<{nframes}h", raw_data)
    samples_normalized = [s / 32768.0 for s in samples]

    samples_per_window = int(framerate * window_ms / 1000)

    rms_values = []
    for i in range(0, len(samples_normalized) - samples_per_window + 1, samples_per_window):
        window = samples_normalized[i:i+samples_per_window]
        rms = math.sqrt(sum(x*x for x in window) / samples_per_window)
        rms_values.append(rms)

    return rms_values

def test_rms_endpoint():
    file_path = "/app/dataset_sample.wav"
    assert os.path.exists(file_path), "Audio file is missing"

    window_ms = 100
    expected_rms = compute_expected_rms(file_path, window_ms)

    url = "http://127.0.0.1:8080/features/rms"
    payload = {"window_ms": window_ms}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Body: {response.text}"

    try:
        actual_rms = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(actual_rms, list), "Expected a JSON array of floats"
    assert len(actual_rms) == len(expected_rms), f"Expected {len(expected_rms)} windows, got {len(actual_rms)}"

    for i, (actual, expected) in enumerate(zip(actual_rms, expected_rms)):
        assert math.isclose(actual, expected, abs_tol=1e-4), f"RMS mismatch at window {i}: expected {expected}, got {actual}"

def test_tune_threshold_endpoint():
    file_path = "/app/dataset_sample.wav"
    assert os.path.exists(file_path), "Audio file is missing"

    window_ms = 100
    threshold = 0.05
    expected_rms = compute_expected_rms(file_path, window_ms)
    expected_active = sum(1 for rms in expected_rms if rms > threshold)

    url = "http://127.0.0.1:8080/tune/threshold"
    payload = {"window_ms": window_ms, "threshold": threshold}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(data, dict), "Expected a JSON object"
    assert "active_windows" in data, "Key 'active_windows' missing in response"

    actual_active = data["active_windows"]
    assert actual_active == expected_active, f"Expected {expected_active} active windows, got {actual_active}"