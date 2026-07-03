# test_final_state.py
import os
import socket
import struct
import json
import pytest

def compute_max_sum(filepath, window_size=500):
    with open(filepath, 'rb') as f:
        f.read(44) # skip header
        data = f.read()

    num_samples = len(data) // 2
    if num_samples == 0:
        return 0

    samples = struct.unpack(f'<{num_samples}h', data)
    abs_samples = [abs(s) for s in samples]

    if num_samples < window_size:
        return sum(abs_samples)

    current_sum = sum(abs_samples[:window_size])
    max_sum = current_sum

    for i in range(window_size, num_samples):
        current_sum += abs_samples[i] - abs_samples[i - window_size]
        if current_sum > max_sum:
            max_sum = current_sum

    return max_sum

def test_server_compiled():
    assert os.path.isfile("/home/user/server"), "The server executable /home/user/server is missing."
    assert os.access("/home/user/server", os.X_OK), "The server executable is not executable."

def test_server_response():
    audio_path = "/app/audio.wav"
    assert os.path.isfile(audio_path), f"Audio file {audio_path} is missing."

    expected_max = compute_max_sum(audio_path, 500)

    host = "127.0.0.1"
    port = 7777

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((host, port))
    except Exception as e:
        pytest.fail(f"Failed to connect to the server at {host}:{port}: {e}")

    request_str = '{"text": "Data \\u03A9"}\n'
    try:
        s.sendall(request_str.encode('utf-8'))
        response_bytes = s.recv(4096)
    except Exception as e:
        s.close()
        pytest.fail(f"Failed to send/receive data: {e}")
    finally:
        s.close()

    assert response_bytes, "Received empty response from the server."

    response_str = response_bytes.decode('utf-8').strip()
    expected_response = f'{{"decoded": "Data Ω", "max_sum": {expected_max}}}'

    assert response_str == expected_response, f"Expected response '{expected_response}', but got '{response_str}'"