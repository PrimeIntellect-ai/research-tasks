# test_final_state.py

import os
import socket
import pytest

def test_embeddings_csv_exists_and_populated():
    csv_path = "/home/user/processed/embeddings.csv"
    assert os.path.isfile(csv_path), f"Embeddings CSV not found at {csv_path}"

    with open(csv_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) >= 5, f"Expected at least 5 lines in embeddings.csv, found {len(lines)}"

    # Check format of a line
    for line in lines:
        parts = line.strip().split(',', 1)
        assert len(parts) == 2, f"Invalid format in embeddings.csv line: {line.strip()}"
        assert parts[0].startswith("frame_") and parts[0].endswith(".jpg"), f"Invalid frame name format: {parts[0]}"

def test_tcp_server_response():
    csv_path = "/home/user/processed/embeddings.csv"
    assert os.path.isfile(csv_path), "Embeddings CSV missing, cannot test server"

    # Find expected embedding for frame 0005
    expected_embedding = None
    with open(csv_path, 'r') as f:
        for line in f:
            if line.startswith("frame_0005.jpg"):
                expected_embedding = line.strip().split(',', 1)[1].strip()
                break

    assert expected_embedding is not None, "frame_0005.jpg not found in embeddings.csv"

    # Connect to the TCP server
    host = '127.0.0.1'
    port = 8888

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((host, port))
            s.sendall(b"0005\n")

            # Read response
            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk

        actual_embedding = response.decode('utf-8').strip()

        assert actual_embedding == expected_embedding, f"Server response '{actual_embedding}' does not match expected '{expected_embedding}'"

    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to TCP server at {host}:{port}. Is it running?")
    except socket.timeout:
        pytest.fail("TCP server connection or read timed out.")