# test_final_state.py
import socket
import pytest

HOST = "127.0.0.1"
PORT = 8333
TIMEOUT = 2.0

def send_command(cmd: str) -> str:
    try:
        with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as s:
            s.sendall(cmd.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response.strip()
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {HOST}:{PORT}. Is the server running?")
    except Exception as e:
        pytest.fail(f"Failed to communicate with server: {e}")

def test_stats_command():
    """Test the STATS command returns correct C and L counts."""
    response = send_command("STATS\n")
    assert response == "C=6 L=25", f"Expected 'C=6 L=25', got '{response}'"

def test_solve_command():
    """Test the SOLVE command returns the correct root."""
    response = send_command("SOLVE\n")
    assert response == "ROOT=5.0000", f"Expected 'ROOT=5.0000', got '{response}'"

def test_quit_command():
    """Test the QUIT command returns BYE."""
    response = send_command("QUIT\n")
    assert response == "BYE", f"Expected 'BYE', got '{response}'"

def test_server_stays_running():
    """Test that the server can handle multiple connections sequentially."""
    # Send STATS twice to ensure it didn't crash after the first
    resp1 = send_command("STATS\n")
    resp2 = send_command("STATS\n")
    assert resp1 == "C=6 L=25"
    assert resp2 == "C=6 L=25"