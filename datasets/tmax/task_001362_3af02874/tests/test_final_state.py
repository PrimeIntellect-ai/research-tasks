# test_final_state.py
import socket
import tarfile
import tempfile
import os
import pytest

def test_stats_request():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(('127.0.0.1', 8888))
            s.sendall(b"REQ: STATS\n")
            response = s.recv(1024).decode('utf-8')
            assert response == "COUNT=117\n", f"Expected COUNT=117\\n, got {repr(response)}"
    except ConnectionRefusedError:
        pytest.fail("Connection refused on 127.0.0.1:8888. Is the server running?")
    except socket.timeout:
        pytest.fail("Socket timeout while waiting for STATS response.")

def test_download_request():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(('127.0.0.1', 8888))
            s.sendall(b"REQ: DOWNLOAD\n")

            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
    except ConnectionRefusedError:
        pytest.fail("Connection refused on 127.0.0.1:8888. Is the server running?")
    except socket.timeout:
        pytest.fail("Socket timeout while receiving DOWNLOAD response.")

    assert len(data) > 0, "No data received for DOWNLOAD request"

    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = os.path.join(tmpdir, "backup.tar.gz")
        with open(tar_path, "wb") as f:
            f.write(data)

        try:
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError as e:
            pytest.fail(f"Downloaded data is not a valid gzip tarball: {e}")

        clean_logs_path = os.path.join(tmpdir, "clean_logs.txt")
        assert os.path.exists(clean_logs_path), "clean_logs.txt not found at the root of the downloaded tarball"

        with open(clean_logs_path, "r") as f:
            lines = f.readlines()

        assert len(lines) == 117, f"Expected 117 lines in clean_logs.txt, got {len(lines)}"
        for line in lines:
            assert line.startswith("DATA: "), f"Line in clean_logs.txt does not start with 'DATA: ': {repr(line)}"