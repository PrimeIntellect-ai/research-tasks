# test_final_state.py
import socket
import pytest

def test_server_valid_patch():
    host = "127.0.0.1"
    port = 8080

    payload = b"VALIDATE SGVsbG8gV29ybGQhCg== LS0tIG9sZC50eHQJMjAyMy0xMC0yNCAxMjozNDo1Ni4wMDAwMDAwMDAgKzAwMDAKKysrIG5ldy50eHQJMjAyMy0xMC0yNCAxMjozNToxMi4wMDAwMDAwMDAgKzAwMDAKQEAgLTEgKzEgQEAKLUhlbGxvIFdvcmxkIQorSGVsbG8gQysrIQo=\n"

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(payload)
            response = s.recv(1024).decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with server at {host}:{port}: {e}")

    assert response == "SUCCESS 7C743489", f"Expected 'SUCCESS 7C743489', but got '{response}'"

def test_server_invalid_patch():
    host = "127.0.0.1"
    port = 8080

    # "fake patch" base64 is ZmFrZSBwYXRjaA==
    payload = b"VALIDATE SGVsbG8gV29ybGQhCg== ZmFrZSBwYXRjaA==\n"

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(payload)
            response = s.recv(1024).decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with server at {host}:{port}: {e}")

    assert response == "ERROR PATCH_FAILED", f"Expected 'ERROR PATCH_FAILED', but got '{response}'"