# test_final_state.py
import os
import socket
import pytest

def send_request(host, port, message):
    try:
        with socket.create_connection((host, port), timeout=2) as sock:
            sock.sendall(message.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with service at {host}:{port}: {e}")

@pytest.mark.parametrize("request_str, expected_response", [
    ("FETCH 104\n", "Admin login ok\n"),
    ("FETCH 102\n", "Erreur system 404!\n"),
    ("FETCH 203\n", "Admin login ok\n"),
    ("FETCH 201\n", "Error system 404!\n"),
    ("FETCH 103\n", "ERROR\n"),
    ("FETCH 202\n", "ERROR\n"),
    ("FETCH 101\n", "ERROR\n"),
    ("FETCH 204\n", "ERROR\n"),
    ("FETCH 999\n", "ERROR\n"),
    ("INVALID CMD\n", "ERROR\n"),
])
def test_tcp_service(request_str, expected_response):
    """Test the TCP service at 127.0.0.1:9090 for correct responses."""
    host = "127.0.0.1"
    port = 9090
    actual_response = send_request(host, port, request_str)
    assert actual_response == expected_response, (
        f"For request {repr(request_str)}, expected {repr(expected_response)} "
        f"but got {repr(actual_response)}"
    )

def test_accepted_translations_file_exists():
    """Test that the final processed dataset is saved to accepted_translations.tsv."""
    file_path = "/home/user/accepted_translations.tsv"
    assert os.path.isfile(file_path), (
        f"File {file_path} is missing. The processed dataset must be saved here."
    )