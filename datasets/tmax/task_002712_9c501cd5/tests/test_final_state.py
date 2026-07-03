# test_final_state.py
import socket
import pytest

HOST = '127.0.0.1'
PORT = 8888

def send_command(cmd: bytes) -> bytes:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect((HOST, PORT))
            s.sendall(cmd)
            data = b""
            while b'\n' not in data:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
            return data
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused. Is the C server running on {HOST}:{PORT}?")
    except socket.timeout:
        pytest.fail(f"Connection or read timed out while communicating with {HOST}:{PORT}.")
    except Exception as e:
        pytest.fail(f"Failed to communicate with server on {HOST}:{PORT}: {e}")

def test_auth_command():
    response = send_command(b"AUTH\n")
    expected = b"ECHO\n"
    assert response == expected, f"AUTH command failed. Expected {expected!r}, got {response!r}"

def test_corrupted_command():
    response = send_command(b"CORRUPTED\n")
    expected = b"archive_02.zip,archive_05.tar.gz\n"
    assert response == expected, f"CORRUPTED command failed. Expected {expected!r}, got {response!r}"

def test_total_bytes_command():
    response = send_command(b"TOTAL_BYTES\n")
    expected = b"8675309\n"
    assert response == expected, f"TOTAL_BYTES command failed. Expected {expected!r}, got {response!r}"