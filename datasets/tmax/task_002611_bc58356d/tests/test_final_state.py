# test_final_state.py
import socket
import pytest

def send_query(name: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        try:
            s.connect(('127.0.0.1', 8080))
        except ConnectionRefusedError:
            pytest.fail("TCP server is not listening on 127.0.0.1:8080. Did you start the server?")

        s.sendall(f"{name}\n".encode('utf-8'))
        response = b""
        while True:
            try:
                chunk = s.recv(4096)
            except socket.timeout:
                pytest.fail("Server timed out while waiting for a response.")
            if not chunk:
                break
            response += chunk
            if b'\n' in chunk:
                break
        return response.decode('utf-8')

def test_alice_query():
    response = send_query("Alice")
    expected = "Databases,Graph Theory,Machine Learning\n"
    assert response == expected, f"Expected {repr(expected)}, but got {repr(response)}"

def test_unknown_user_query():
    response = send_query("UnknownUser")
    # Should be empty or just a newline since UnknownUser knows nobody
    assert response in ("", "\n"), f"Expected empty response or newline for unknown user, but got {repr(response)}"