# test_final_state.py
import socket
import time
import pytest

HOST = "127.0.0.1"
PORT = 9090

def test_auth_failure():
    """Test that the server drops the connection on invalid auth."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect((HOST, PORT))
        s.sendall(b"ETL_AUTH: INVALID\n")
        # The server should close the connection
        data = s.recv(1024)
        assert data == b"", "Server should drop connection on invalid auth, but returned data."
    except ConnectionRefusedError:
        pytest.fail("Server is not running on 127.0.0.1:9090")
    finally:
        s.close()

def test_pipeline_success():
    """Test the full ETL pipeline with valid auth, embedded newlines, and reshaping."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        pytest.fail("Server is not running on 127.0.0.1:9090")

    try:
        # Send auth
        s.sendall(b"ETL_AUTH: VALID_STR_8472\n")

        # Send CSV data. The dummy processor flags lines with "9.9"
        # The timestamp 2023-10-12T10:00:00Z corresponds to 1697104800
        csv_data = (
            '2023-10-12T09:00:00Z,1.0,2.0,3.0,"Normal note"\n'
            '2023-10-12T10:00:00Z,9.9,1.1,2.2,"Note with\na newline"\n'
        )
        s.sendall(csv_data.encode("utf-8"))

        # We need to signal EOF to the server so it stops reading and processes the data
        s.shutdown(socket.SHUT_WR)

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

        response_str = response.decode("utf-8")

        assert "EOF_PIPELINE" in response_str, "Response did not end with EOF_PIPELINE"

        # Check if the newline was cleaned
        assert "Note with a newline" in response_str or "Note withnewline" in response_str or "Note with\ta newline" not in response_str, "Embedded newline was not properly handled."

        # Check if it was reshaped to long format
        assert "Sensor1" in response_str, "Missing Sensor1 in long format."
        assert "Sensor2" in response_str, "Missing Sensor2 in long format."
        assert "Sensor3" in response_str, "Missing Sensor3 in long format."
        assert "2023-10-12T10:00:00Z" in response_str, "Missing or incorrect timestamp in output."

    finally:
        s.close()