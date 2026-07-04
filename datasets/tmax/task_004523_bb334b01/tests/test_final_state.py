# test_final_state.py

import os
import socket
import pytest

HOST = "127.0.0.1"
PORT = 8050

def send_query_and_get_response(query: str) -> str:
    try:
        with socket.create_connection((HOST, PORT), timeout=2.0) as s:
            s.sendall(query.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {HOST}:{PORT}. Is the server running?")
    except socket.timeout:
        pytest.fail(f"Connection to {HOST}:{PORT} timed out waiting for a response.")
    except Exception as e:
        pytest.fail(f"Unexpected error communicating with server: {e}")

def test_server_source_and_binary_exist():
    assert os.path.exists("/home/user/search_server.c"), "The C source code /home/user/search_server.c is missing."
    assert os.path.exists("/home/user/search_server"), "The compiled binary /home/user/search_server is missing."
    assert os.access("/home/user/search_server", os.X_OK), "The binary /home/user/search_server is not executable."

def test_query_omega_backup():
    response = send_query_and_get_response("omega_backup\n")
    assert response == "MATCH: fileB.zdat\n", f"Expected 'MATCH: fileB.zdat\\n' but got {repr(response)}"

def test_query_alpha_core():
    response = send_query_and_get_response("alpha_core\n")
    assert response == "MATCH: fileA.zdat\n", f"Expected 'MATCH: fileA.zdat\\n' but got {repr(response)}"

def test_query_zeta_frontend():
    response = send_query_and_get_response("zeta_frontend\n")
    assert response == "MATCH: fileC.zdat\n", f"Expected 'MATCH: fileC.zdat\\n' but got {repr(response)}"

def test_query_nonexistent_proj():
    response = send_query_and_get_response("nonexistent_proj\n")
    assert response == "NONE\n", f"Expected 'NONE\\n' but got {repr(response)}"