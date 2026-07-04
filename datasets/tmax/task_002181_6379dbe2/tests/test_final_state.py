# test_final_state.py
import socket
import struct
import pytest

def test_backup_daemon_protocol():
    host = '127.0.0.1'
    port = 9090

    try:
        s = socket.create_connection((host, port), timeout=5)
    except Exception as e:
        pytest.fail(f"Could not connect to daemon on {host}:{port}: {e}")

    with s:
        # Send AUTH
        s.sendall(b"AUTH: gamma ray burst\n")

        # Send BACKUP
        s.sendall(b"BACKUP\n")

        def recv_exact(sock, n):
            data = bytearray()
            while len(data) < n:
                packet = sock.recv(n - len(data))
                if not packet:
                    return None
                data.extend(packet)
            return bytes(data)

        files_received = {}

        while True:
            path_len_bytes = recv_exact(s, 2)
            if not path_len_bytes:
                pytest.fail("Connection closed unexpectedly before end of stream marker.")

            path_len = struct.unpack('<H', path_len_bytes)[0]
            if path_len == 0:
                # End of stream indicated by 0x00 0x00
                break

            path_bytes = recv_exact(s, path_len)
            if not path_bytes:
                pytest.fail("Failed to read file path from stream.")
            path = path_bytes.decode('utf-8', errors='replace')

            size_bytes = recv_exact(s, 4)
            if not size_bytes:
                pytest.fail("Failed to read file size from stream.")
            size = struct.unpack('<I', size_bytes)[0]

            file_data = recv_exact(s, size) if size > 0 else b""
            if size > 0 and not file_data:
                pytest.fail(f"Failed to read file data for {path}.")

            files_received[path] = file_data

    found_file1 = False
    found_file2 = False

    for path, data in files_received.items():
        if path.endswith("file1.txt"):
            assert b"Important data 1" in data, f"Incorrect data in {path}"
            found_file1 = True
        elif path.endswith("file2.txt"):
            assert b"Important data 2" in data, f"Incorrect data in {path}"
            found_file2 = True
        else:
            pytest.fail(f"Unexpected file in backup stream (symlink loop not handled correctly?): {path}")

    assert found_file1, "file1.txt was not found in the backup stream."
    assert found_file2, "file2.txt was not found in the backup stream."

def test_backup_daemon_bad_auth():
    host = '127.0.0.1'
    port = 9090

    try:
        s = socket.create_connection((host, port), timeout=5)
    except Exception as e:
        pytest.fail(f"Could not connect to daemon on {host}:{port}: {e}")

    with s:
        s.sendall(b"AUTH: wrong password\n")

        # The connection should be closed by the server
        try:
            data = s.recv(1024)
            assert not data, "Server should close connection on invalid auth but returned data."
        except ConnectionResetError:
            pass # Expected