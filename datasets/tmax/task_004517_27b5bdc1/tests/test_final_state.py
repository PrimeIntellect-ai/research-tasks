# test_final_state.py

import socket
import pytest

def query_server(name: str) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect(('127.0.0.1', 8888))
            s.sendall(f"{name}\n".encode('utf-8'))
            data = s.recv(1024)
            return data.decode('utf-8').strip()
    except ConnectionRefusedError:
        pytest.fail("Server is not listening on 127.0.0.1:8888. Did you leave it running in the background?")
    except socket.timeout:
        pytest.fail(f"Server timed out when querying for {name}.")
    except Exception as e:
        pytest.fail(f"Unexpected error communicating with server: {e}")

def test_bob_subordinates():
    response = query_server("Bob")
    assert response == "10", f"Expected 10 for Bob, got {response}. Ensure you are bypassing the corrupted index and correctly summing transitive subordinates."

def test_alice_subordinates():
    response = query_server("Alice")
    assert response == "17", f"Expected 17 for Alice, got {response}. Ensure you are bypassing the corrupted index and correctly summing transitive subordinates."

def test_frank_subordinates():
    response = query_server("Frank")
    assert response == "2", f"Expected 2 for Frank, got {response}."

def test_dave_subordinates():
    response = query_server("Dave")
    assert response == "1", f"Expected 1 for Dave, got {response}."