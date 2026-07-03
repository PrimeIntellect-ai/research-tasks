# test_final_state.py

import socket
import pytest

HOST = '127.0.0.1'
PORT = 8080
AUTH_TOKEN = "AUTH: ecoweb2024\n"

def send_and_receive(sock, message):
    sock.sendall(message.encode('utf-8'))
    # Read until newline
    response = b""
    while b"\n" not in response:
        chunk = sock.recv(1024)
        if not chunk:
            break
        response += chunk
    return response.decode('utf-8')

def test_server_auth_and_queries():
    """Connect to the server, authenticate, and test queries."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            # Send Auth
            sock.sendall(AUTH_TOKEN.encode('utf-8'))

            # Test Fox
            resp = send_and_receive(sock, "MATCH Fox\n")
            assert resp == "Mouse,Rabbit\n", f"Expected 'Mouse,Rabbit\\n' for Fox, got {repr(resp)}"

            # Test Owl
            resp = send_and_receive(sock, "MATCH Owl\n")
            assert resp == "Fox,Mouse\n", f"Expected 'Fox,Mouse\\n' for Owl, got {repr(resp)}"

            # Test Rabbit
            resp = send_and_receive(sock, "MATCH Rabbit\n")
            assert resp == "Grass\n", f"Expected 'Grass\\n' for Rabbit, got {repr(resp)}"

            # Test Grass
            resp = send_and_receive(sock, "MATCH Grass\n")
            assert resp == "NONE\n", f"Expected 'NONE\\n' for Grass, got {repr(resp)}"

            # Test Bear
            resp = send_and_receive(sock, "MATCH Bear\n")
            assert resp == "NONE\n", f"Expected 'NONE\\n' for Bear, got {repr(resp)}"

    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}. Is it running?")
    except socket.timeout:
        pytest.fail("Server connection or response timed out.")

def test_server_bad_auth():
    """Test that the server drops the connection on bad authentication."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.sendall(b"AUTH: badtoken\n")

            # Try to send a command
            try:
                sock.sendall(b"MATCH Fox\n")
                resp = sock.recv(1024)
                assert resp == b"", f"Server should close connection on bad auth, but responded: {resp}"
            except (ConnectionResetError, BrokenPipeError):
                # This is expected behavior
                pass
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}. Is it running?")