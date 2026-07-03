# test_final_state.py

import os
import socket
import re
import pytest

def test_mount_and_restored_file():
    # Check if mounted
    with open('/proc/mounts', 'r') as f:
        mounts = f.read()
    assert '/app/dataset' in mounts or '/app/cnc_data.ext4' in mounts, "The ext4 image is not mounted at /app/dataset"

    # Check restored file
    job_file = "/app/restored/job.gcode"
    assert os.path.exists(job_file), f"{job_file} does not exist"

    with open(job_file, 'r') as f:
        content = f.read()
    assert "; SYNC T=00:00:07 Z=3.5" in content, "The restored job.gcode does not contain the expected update.tar content"

def test_tcp_server_extract_success():
    host = '127.0.0.1'
    port = 7777

    # Connect and send valid request
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        try:
            s.connect((host, port))
        except Exception as e:
            pytest.fail(f"Failed to connect to server on {host}:{port} - {e}")

        s.sendall(b"EXTRACT Z=3.5\n")
        response = s.recv(1024).decode('utf-8')

    match = re.match(r"^SUCCESS T=00:00:07 BYTES=(\d+)\n?$", response.strip())
    assert match is not None, f"Server response did not match expected success format. Got: {response}"

    bytes_reported = int(match.group(1))

    # Verify file exists and size matches
    frame_path = "/app/frames/frame_3.5.jpg"
    assert os.path.exists(frame_path), f"Frame image {frame_path} was not created"

    actual_size = os.path.getsize(frame_path)
    assert actual_size == bytes_reported, f"Reported size ({bytes_reported}) does not match actual file size ({actual_size})"

def test_tcp_server_extract_not_found():
    host = '127.0.0.1'
    port = 7777

    # Connect and send invalid request
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        try:
            s.connect((host, port))
        except Exception as e:
            pytest.fail(f"Failed to connect to server on {host}:{port} - {e}")

        s.sendall(b"EXTRACT Z=9.9\n")
        response = s.recv(1024).decode('utf-8')

    assert response.strip() == "ERROR NOT_FOUND", f"Server response did not match expected error format. Got: {response}"