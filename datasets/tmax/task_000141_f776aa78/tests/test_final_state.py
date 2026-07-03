# test_final_state.py
import os
import socket
import zipfile
import io
import time
import pytest
import requests

def test_tcp_server_count():
    """Test the TCP server on port 9090 for the COUNT command."""
    with socket.create_connection(("127.0.0.1", 9090), timeout=5) as sock:
        sock.sendall(b"COUNT\n")
        response = sock.recv(1024).decode('utf-8')
        assert response.endswith("\n"), "COUNT response must end with a newline"
        count_str = response.strip()
        assert count_str.isdigit(), f"COUNT response must be a number, got: {count_str}"
        assert int(count_str) > 0, "COUNT must be greater than 0 since the generator is running"

def test_tcp_server_latest():
    """Test the TCP server on port 9090 for the LATEST command."""
    with socket.create_connection(("127.0.0.1", 9090), timeout=5) as sock:
        sock.sendall(b"LATEST\n")
        response = sock.recv(1024).decode('utf-8')
        assert response.endswith("\n"), "LATEST response must end with a newline"
        latest_str = response.strip()
        assert latest_str.startswith("archive_") and latest_str.endswith(".zip"), f"LATEST response must be an archive filename, got: {latest_str}"

def test_http_server_and_archive_validation():
    """Test the HTTP server on port 8080 and validate the latest.zip archive."""
    url = "http://127.0.0.1:8080/latest.zip"

    # Retry logic in case the file is just being written
    for _ in range(5):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                break
        except requests.RequestException:
            pass
        time.sleep(1)
    else:
        pytest.fail(f"Failed to fetch {url} via HTTP GET")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    # Read the ZIP file from memory
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            file_list = z.namelist()
            assert len(file_list) > 0, "The ZIP archive is empty"

            # Sort files to check chunk sizes
            file_list.sort()

            for i, filename in enumerate(file_list):
                info = z.getinfo(filename)
                # All chunks except possibly the last one must be exactly 102,400 bytes
                if i < len(file_list) - 1:
                    assert info.file_size == 102400, f"Chunk {filename} is {info.file_size} bytes, expected 102400 bytes"
                else:
                    assert info.file_size <= 102400, f"Last chunk {filename} is {info.file_size} bytes, expected <= 102400 bytes"

    except zipfile.BadZipFile:
        pytest.fail("The downloaded payload is not a valid ZIP archive")

def test_cleanup_performed():
    """Check that cleanup is being performed on processed files."""
    raw_logs_dir = "/home/user/raw_logs/"
    assert os.path.isdir(raw_logs_dir), f"Directory {raw_logs_dir} does not exist"

    # There shouldn't be a huge accumulation of .done files if cleanup is working
    # Since the generator creates one every 5 seconds, there might be 1 or 2 currently processing
    done_files = [f for f in os.listdir(raw_logs_dir) if f.endswith(".done")]
    assert len(done_files) < 10, "Cleanup does not appear to be working; too many .done files left behind"