# test_final_state.py

import os
import socket
import pytest

HOST = '127.0.0.1'
PORT = 9090

def test_server_source_and_binary_exist():
    """Test that the C source and compiled binary exist."""
    assert os.path.exists('/home/user/config_server.c'), "Source file /home/user/config_server.c is missing."
    assert os.path.exists('/home/user/config_server'), "Compiled binary /home/user/config_server is missing."
    assert os.access('/home/user/config_server', os.X_OK), "Binary /home/user/config_server is not executable."

def test_server_dump_output():
    """Test the DUMP command on the server to verify the final configuration state."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(b"DUMP\n")

            # Read response
            response = b""
            while b"END\n" not in response:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk

            response_str = response.decode('utf-8')
            lines = [line.strip() for line in response_str.strip().split('\n') if line.strip()]

            assert lines, "Received empty response from DUMP command."
            assert lines[-1] == "END", "Response did not end with 'END'."

            config_lines = lines[:-1]

            expected_configs = {
                "CONFIG: key=timeout value=120 admin=***",
                "CONFIG: key=retries value=5 admin=***",
                "CONFIG: key=max_connections value=1000 admin=***"
            }

            actual_configs = set(config_lines)

            missing = expected_configs - actual_configs
            extra = actual_configs - expected_configs

            assert not missing, f"Missing expected configurations: {missing}"
            assert not extra, f"Unexpected configurations found: {extra}"
            assert len(config_lines) == len(expected_configs), "Duplicate configurations found in DUMP output."

    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}. Is it running?")
    except socket.timeout:
        pytest.fail("Connection or read timed out.")

def test_server_add_validation():
    """Test that the server correctly validates and masks new ADD commands."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            # Send an invalid value (negative)
            s.sendall(b"ADD key=test_neg value=-5 admin=Alice\n")
            ack1 = s.recv(1024).decode('utf-8')
            # It might send ACK or drop it, but it shouldn't store it.

            # Send a valid value
            s.sendall(b"ADD key=test_pos value=42 admin=Bob\n")
            ack2 = s.recv(1024).decode('utf-8')
            assert "ACK" in ack2, "Server did not acknowledge valid ADD command."

        # Reconnect to DUMP and verify
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(b"DUMP\n")
            response = b""
            while b"END\n" not in response:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk

            response_str = response.decode('utf-8')

            assert "CONFIG: key=test_pos value=42 admin=***" in response_str, "Valid config was not stored or masked correctly."
            assert "test_neg" not in response_str, "Invalid config (negative value) was incorrectly stored."

    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}. Is it running?")
    except socket.timeout:
        pytest.fail("Connection or read timed out.")