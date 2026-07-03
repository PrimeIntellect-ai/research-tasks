# test_final_state.py

import os
import subprocess
import json
import zlib
import requests
import pytest

def test_c_code_fixed():
    path = "/home/user/src/checksum.c"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, 'r') as f:
        content = f.read()
    assert "i <= len" not in content, f"File {path} still contains the OOB read bug (i <= len)."
    assert "i < len" in content, f"File {path} does not appear to be fixed correctly."

def test_server_arm64_binary():
    path = "/home/user/build/server_arm64"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'rb') as f:
        header = f.read(20)

    assert header[:4] == b'\x7fELF', f"File {path} is not a valid ELF binary."
    # Machine type at offset 18
    machine = header[18:20]
    assert machine == b'\xb7\x00', f"File {path} is not an ARM64 binary."

def test_server_amd64_binary():
    path = "/home/user/build/server_amd64"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'rb') as f:
        header = f.read(20)

    assert header[:4] == b'\x7fELF', f"File {path} is not a valid ELF binary."
    # Machine type at offset 18
    machine = header[18:20]
    assert machine == b'\x3e\x00', f"File {path} is not an AMD64 binary."

def test_benchmark_output():
    path = "/home/user/bench.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, 'r') as f:
        content = f.read()
    assert "Benchmark" in content or "ns/op" in content, f"File {path} does not contain valid Go benchmark output."

def test_http_service_process():
    video_path = "/app/test_video.mp4"
    assert os.path.exists(video_path), "Test video file is missing."

    # Calculate expected checksum
    cmd = [
        "ffmpeg", "-i", video_path, "-vframes", "10", 
        "-f", "image2pipe", "-vcodec", "rawvideo", 
        "-pix_fmt", "rgb24", "-"
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        raw_data = proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ffmpeg to calculate expected checksum: {e.stderr.decode()}")

    expected_checksum = zlib.adler32(raw_data) & 0xffffffff

    # Send request to the Go service
    url = "http://127.0.0.1:8080/process"
    payload = {"video_path": video_path}
    try:
        response = requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "checksum" in data, f"Response JSON does not contain 'checksum' key: {data}"

    actual_checksum = data["checksum"]
    assert actual_checksum == expected_checksum, f"Expected checksum {expected_checksum}, got {actual_checksum}."