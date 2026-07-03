# test_final_state.py

import socket
import re
import pytest

def send_command(cmd: str) -> str:
    """Send a command to the TCP server and return the response."""
    try:
        with socket.create_connection(("127.0.0.1", 9090), timeout=5.0) as sock:
            sock.sendall(cmd.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with server on 127.0.0.1:9090: {e}")

def test_frame_30_inactive():
    """Test that frame 30 (which is black) returns a very low probability of being active."""
    response = send_command("FRAME 30\n")
    match = re.match(r"^PROB:\s+([0-9.]+)\n?$", response)
    assert match is not None, f"Unexpected response format for FRAME 30: {response!r}"
    prob = float(match.group(1))
    assert prob < 0.0010, f"Expected probability for frame 30 to be < 0.0010, got {prob}"

def test_count_inactive():
    """Test that the server counts exactly 11 inactive frames."""
    response = send_command("COUNT_INACTIVE\n")
    assert response.strip() == "INACTIVE: 11", f"Expected 'INACTIVE: 11', got {response!r}"

def test_frame_5_active():
    """Test that frame 5 (which is normal) returns a very high probability of being active."""
    response = send_command("FRAME 5\n")
    match = re.match(r"^PROB:\s+([0-9.]+)\n?$", response)
    assert match is not None, f"Unexpected response format for FRAME 5: {response!r}"
    prob = float(match.group(1))
    assert prob > 0.9990, f"Expected probability for frame 5 to be > 0.9990, got {prob}"