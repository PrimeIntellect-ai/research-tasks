# test_final_state.py

import socket
import pytest

def send_request(client_id, timeout=5.0):
    """Helper to send a GET request to the TCP server and read the response."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(('127.0.0.1', 9000))
        s.sendall(f"GET {client_id}\n".encode('utf-8'))

        response = b""
        while b"END\n" not in response:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        s.close()
        return response.decode('utf-8').replace('\r\n', '\n')
    except ConnectionRefusedError:
        pytest.fail("Connection refused. Ensure the TCP server is running on 127.0.0.1:9000.")
    except socket.timeout:
        pytest.fail("Socket timeout. The server did not respond with 'END\\n' in time.")
    except Exception as e:
        pytest.fail(f"Network error: {e}")

def test_server_active_client_c001():
    """Test that the server returns correct transactions for active client C001."""
    response = send_request("C001")
    expected_lines = [
        "TX1001,150.50,227fa2fcddf6a",
        "TX1002,200.00,227fa32ab89fb",
        "END"
    ]

    actual_lines = [line for line in response.split('\n') if line.strip()]

    assert actual_lines == expected_lines, f"Expected output for C001 to be {expected_lines}, but got {actual_lines}"

def test_server_suspended_client_c002():
    """Test that the server returns only END for suspended client C002."""
    response = send_request("C002")
    actual_lines = [line for line in response.split('\n') if line.strip()]

    assert actual_lines == ["END"], f"Expected output for suspended client C002 to be ['END'], but got {actual_lines}"

def test_server_active_client_c003():
    """Test that the server returns correct transactions for active client C003."""
    response = send_request("C003")
    expected_lines = [
        "TX1004,500.00,227fa3d666299",
        "TX1005,10.00,9f30327f31c7",
        "END"
    ]

    actual_lines = [line for line in response.split('\n') if line.strip()]

    assert actual_lines == expected_lines, f"Expected output for C003 to be {expected_lines}, but got {actual_lines}"

def test_server_nonexistent_client():
    """Test that the server returns only END for a client that does not exist."""
    response = send_request("NONEXISTENT")
    actual_lines = [line for line in response.split('\n') if line.strip()]

    assert actual_lines == ["END"], f"Expected output for nonexistent client to be ['END'], but got {actual_lines}"