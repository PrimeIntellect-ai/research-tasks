# test_final_state.py

import socket
import pytest

HOST = "127.0.0.1"
PORT = 8888
PASSCODE = "849302"

EXPECTED_CSV = """ServerName,ConfigKey,ConfigValue
prod-srv-01,CACHE_SIZE,1024
prod-srv-01,DB_PASSWORD,***
prod-srv-01,OS_VERSION,Ubuntu 22.04
win-srv-02,ADMIN_USER,sysadmin
win-srv-02,API_TOKEN,***
win-srv-02,MAX_WORKERS,64
"""

def test_tcp_server_incorrect_passcode():
    """Test that the server drops connection on incorrect passcode."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(b"000000\n")
            response = s.recv(4096)
            # Either no response or connection closed
            assert response == b"", f"Expected connection to be dropped, but got: {response}"
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to TCP server at {HOST}:{PORT}")
    except socket.timeout:
        pytest.fail("Server timed out without dropping the connection for an invalid passcode.")

def test_tcp_server_correct_passcode():
    """Test that the server returns the correct CSV data on correct passcode."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(f"{PASSCODE}\n".encode('utf-8'))

            response_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk

        response_str = response_data.decode('utf-8').replace('\r\n', '\n')

        assert response_str.strip() == EXPECTED_CSV.strip(), (
            f"Expected CSV response:\n{EXPECTED_CSV}\n\n"
            f"Actual CSV response:\n{response_str}"
        )
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to TCP server at {HOST}:{PORT}")
    except socket.timeout:
        pytest.fail("Server timed out while sending data.")
    except UnicodeDecodeError:
        pytest.fail("Server response was not valid UTF-8.")