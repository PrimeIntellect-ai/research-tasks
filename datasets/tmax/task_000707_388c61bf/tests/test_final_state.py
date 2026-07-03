# test_final_state.py

import os
import tarfile
import hashlib
import socket
import requests
import io
import pytest

def test_services():
    # 1. Test HTTP service
    try:
        response = requests.get("http://127.0.0.1:8080/backup.tar", timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.fail(f"Failed to fetch /backup.tar from HTTP service: {e}")

    tar_content = response.content

    # Verify it's a valid tar file and contains exactly the expected files
    try:
        with tarfile.open(fileobj=io.BytesIO(tar_content), mode="r:*") as tar:
            members = tar.getnames()
            # The files might be flat or inside a directory
            basenames = [os.path.basename(m) for m in members if not tar.getmember(m).isdir() and os.path.basename(m)]
            assert set(basenames) == {"file1.log", "large_file.bin"}, f"Tar file contains incorrect files: {basenames}"
    except tarfile.TarError as e:
        pytest.fail(f"Downloaded content is not a valid tar file: {e}")

    # Compute SHA-256
    expected_hash = hashlib.sha256(tar_content).hexdigest()

    # 2. Test TCP service with correct transcript
    try:
        with socket.create_connection(("127.0.0.1", 9090), timeout=5) as s:
            s.sendall(b"delta protocol override\n")
            data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
            response_text = data.decode('utf-8')
            assert response_text.strip() == expected_hash, f"TCP service returned {response_text.strip()} instead of expected hash {expected_hash}"
    except (socket.error, socket.timeout) as e:
        pytest.fail(f"Failed to connect or communicate with TCP service on port 9090: {e}")

    # 3. Test TCP service with wrong string
    try:
        with socket.create_connection(("127.0.0.1", 9090), timeout=5) as s:
            s.sendall(b"random guess\n")
            data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
            response_text = data.decode('utf-8')
            assert response_text == "DENIED\n", f"TCP service returned {repr(response_text)} instead of 'DENIED\\n'"
    except (socket.error, socket.timeout) as e:
        pytest.fail(f"Failed to connect or communicate with TCP service on port 9090 for DENIED check: {e}")