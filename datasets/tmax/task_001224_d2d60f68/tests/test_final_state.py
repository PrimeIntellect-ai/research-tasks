# test_final_state.py

import os
import wave
import struct
import math
import socket
import pytest

def get_expected_features(wav_path):
    with wave.open(wav_path, 'rb') as wf:
        num_frames = wf.getnframes()
        raw_data = wf.readframes(num_frames)

    samples = struct.unpack(f"<{num_frames}h", raw_data)

    if not samples:
        return 0.0, 0.0, 0.0, 0.0

    avg_amp = sum(abs(s) for s in samples) / num_frames
    max_amp = float(max(abs(s) for s in samples))

    zcr = 0
    for i in range(1, num_frames):
        if (samples[i] >= 0 and samples[i-1] < 0) or (samples[i] < 0 and samples[i-1] >= 0):
            zcr += 1
    zcr_rate = zcr / num_frames

    rms = math.sqrt(sum(s*s for s in samples) / num_frames)

    return avg_amp, max_amp, zcr_rate, rms

def test_pipeline_results_exist():
    """Check that the script generated the results file."""
    assert os.path.isfile("/app/experiment_results.txt"), "Missing /app/experiment_results.txt"

def test_tcp_server_response():
    """Test the TCP server's embedding retrieval logic."""
    wav_path = "/app/fixture.wav"
    assert os.path.isfile(wav_path), f"Missing {wav_path}"

    expected_features = get_expected_features(wav_path)

    query = [10.0, 20.0, 30.0, 40.0]
    expected_distance = math.sqrt(sum((ef - q)**2 for ef, q in zip(expected_features, query)))

    query_str = f"{query[0]},{query[1]},{query[2]},{query[3]}\n"

    try:
        with socket.create_connection(("127.0.0.1", 8080), timeout=5) as sock:
            sock.sendall(query_str.encode("utf-8"))
            response = sock.recv(1024).decode("utf-8")
    except ConnectionRefusedError:
        pytest.fail("TCP server is not listening on 127.0.0.1:8080")
    except socket.timeout:
        pytest.fail("TCP server timed out or did not respond")

    assert response.startswith("Distance: "), f"Unexpected response format: {response}"

    try:
        dist_str = response.strip().split("Distance: ")[1]
        actual_distance = float(dist_str)
    except (IndexError, ValueError):
        pytest.fail(f"Could not parse distance from response: {response}")

    assert math.isclose(actual_distance, expected_distance, rel_tol=1e-3, abs_tol=1e-2), \
        f"Expected distance ~{expected_distance:.4f}, but got {actual_distance:.4f}"