# test_final_state.py
import socket
import requests
import pytest
import time

def test_tcp_admin_check():
    """Test the TCP Admin service."""
    host = '127.0.0.1'
    port = 8081

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"PING\n")
            response = s.recv(1024).decode('utf-8')
            assert response.strip() == "PONG", f"Expected PONG, got {response!r}"
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to TCP Admin service at {host}:{port}. Is the server running?")
    except socket.timeout:
        pytest.fail(f"Connection timed out to TCP Admin service at {host}:{port}.")

def test_http_upload_and_download():
    """Test the HTTP upload with spaces in filename and subsequent download."""
    host = '127.0.0.1'
    port = 8080
    base_url = f"http://{host}:{port}"
    headers = {"Authorization": "Bearer dev-token-123"}

    filename = "test file spaces.txt"
    file_content = b"This is a test file with spaces in the name."

    # 1. Upload
    files = {'file': (filename, file_content)}
    try:
        upload_resp = requests.post(f"{base_url}/upload", headers=headers, files=files, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Connection error when connecting to HTTP service at {base_url}. Is the server running?")

    assert upload_resp.status_code == 200, f"Upload failed with status {upload_resp.status_code}: {upload_resp.text}"

    # 2. Download
    try:
        download_resp = requests.get(f"{base_url}/artifact/{filename}", headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Connection error when downloading from HTTP service at {base_url}.")

    assert download_resp.status_code == 200, f"Download failed with status {download_resp.status_code}: {download_resp.text}"
    assert download_resp.content == file_content, "Downloaded content does not match uploaded content."