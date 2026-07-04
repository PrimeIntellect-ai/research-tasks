# test_final_state.py
import os
import wave
import requests
import numpy as np
import pytest

def test_alert_quiet_file_exists():
    """Verify the processed file was saved to the correct location."""
    file_path = "/home/user/alert_quiet.wav"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_web_server_and_port_forward():
    """Verify that the web server is running, port forwarding works, and the served audio is correct."""
    url = "http://127.0.0.1:9090/alert_quiet.wav"

    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Ensure the C web server and socat port forwarding are running. Error: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}"

    content_type = resp.headers.get("Content-Type", "")
    assert "audio/wav" in content_type.lower(), f"Expected Content-Type 'audio/wav', got '{content_type}'"

    recv_path = "/tmp/test_received.wav"
    with open(recv_path, "wb") as f:
        f.write(resp.content)

    orig_path = "/app/alert_raw.wav"
    assert os.path.exists(orig_path), f"Original file {orig_path} is missing."

    try:
        with wave.open(orig_path, "rb") as w_in:
            frames = w_in.readframes(w_in.getnframes())
            orig_samples = np.frombuffer(frames, dtype=np.int16)
            ref_samples = np.trunc(orig_samples / 2.0).astype(np.int16)
    except Exception as e:
        pytest.fail(f"Error reading original WAV file: {e}")

    try:
        with wave.open(recv_path, "rb") as w_recv:
            recv_frames = w_recv.readframes(w_recv.getnframes())
            recv_samples = np.frombuffer(recv_frames, dtype=np.int16)
    except Exception as e:
        pytest.fail(f"Error reading received WAV file (is it a valid WAV?): {e}")

    assert len(recv_samples) > 0, "Received WAV file has no audio samples."

    # Compute MSE
    min_len = min(len(ref_samples), len(recv_samples))

    # Ensure length is exactly as expected
    assert len(recv_samples) == len(ref_samples), f"Expected {len(ref_samples)} samples, got {len(recv_samples)}."

    mse = np.mean((ref_samples[:min_len].astype(np.float32) - recv_samples[:min_len].astype(np.float32))**2)

    assert mse <= 1.0, f"MSE of audio samples is {mse:.4f}, which exceeds the threshold of 1.0. Ensure the volume was reduced by exactly 50%."