# test_final_state.py

import os
import socket
import tarfile
import io
import time
import pytest

HOST = "127.0.0.1"
PORT = 8080
EXTRACT_DIR = "/home/user/projects/extracted"

def create_tar_gz(files):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for name, content in files.items():
            info = tarfile.TarInfo(name=name)
            info.size = len(content)
            tar.addfile(info, io.BytesIO(content))
    return buf.getvalue()

def send_payload(payload):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((HOST, PORT))
            s.sendall(payload)
            s.shutdown(socket.SHUT_WR)

            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data
        return response.decode('utf-8', errors='replace')
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to daemon on {HOST}:{PORT}. Is it running?")
    except socket.timeout:
        pytest.fail("Socket connection timed out.")

def test_valid_archive():
    payload = create_tar_gz({"project/file.txt": b"valid content"})
    send_payload(payload)

    extracted_file = os.path.join(EXTRACT_DIR, "project", "file.txt")

    # Allow a brief moment for the extraction to complete
    time.sleep(0.5)

    assert os.path.isfile(extracted_file), f"Valid file was not extracted to {extracted_file}."
    with open(extracted_file, "rb") as f:
        assert f.read() == b"valid content", "Extracted file content mismatch."

def test_malicious_archive_rejected():
    payload = create_tar_gz({"project/../../home/user/hacked.txt": b"malicious content"})
    response = send_payload(payload)

    assert "ERROR: Path traversal detected" in response, (
        f"Expected exact error message 'ERROR: Path traversal detected', but got: {response}"
    )

    hacked_file = "/home/user/hacked.txt"
    assert not os.path.exists(hacked_file), f"Malicious file was extracted to {hacked_file}!"

def test_absolute_path_malicious_archive_rejected():
    payload = create_tar_gz({"/tmp/absolute_hack.txt": b"absolute path content"})
    response = send_payload(payload)

    assert "ERROR: Path traversal detected" in response, (
        f"Expected exact error message 'ERROR: Path traversal detected' for absolute path, but got: {response}"
    )

    hacked_file = "/tmp/absolute_hack.txt"
    assert not os.path.exists(hacked_file), f"Malicious absolute path file was extracted to {hacked_file}!"