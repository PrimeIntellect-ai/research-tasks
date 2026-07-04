# test_final_state.py

import socket
import zlib
import struct
import subprocess
import hashlib
import pytest

HOST = '127.0.0.1'
PORT = 8888

def send_command(cmd: str) -> bytes:
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as s:
            s.sendall(cmd.encode('utf-8'))
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
            return data
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}. Is it running?")
    except socket.timeout:
        pytest.fail(f"Timeout while waiting for response to command: {cmd.strip()}")
    except Exception as e:
        pytest.fail(f"Error communicating with server: {e}")

def test_backup_command():
    raw_response = send_command("BACKUP\n")
    assert raw_response, "Received empty response for BACKUP command"

    try:
        decompressed = zlib.decompress(raw_response)
    except zlib.error as e:
        pytest.fail(f"Failed to zlib decompress BACKUP response: {e}")

    offset = 0
    files = {}

    while offset < len(decompressed):
        if offset + 2 > len(decompressed):
            pytest.fail("Truncated archive: missing path length")
        path_len = struct.unpack_from("<H", decompressed, offset)[0]
        offset += 2

        if offset + path_len > len(decompressed):
            pytest.fail("Truncated archive: missing path string")
        path = decompressed[offset:offset+path_len].decode('utf-8')
        offset += path_len

        if offset + 4 > len(decompressed):
            pytest.fail("Truncated archive: missing file size")
        file_size = struct.unpack_from("<I", decompressed, offset)[0]
        offset += 4

        if offset + file_size > len(decompressed):
            pytest.fail("Truncated archive: missing file content")
        content = decompressed[offset:offset+file_size]
        offset += file_size

        files[path] = content

    expected_files = {
        "main.json": b'{"app": "v1.0", "debug": true}',
        "secrets.txt": b'super_secret_key_123'
    }

    # The paths might have a leading slash or dot, let's normalize them
    normalized_files = {k.lstrip('./'): v for k, v in files.items()}

    for expected_path, expected_content in expected_files.items():
        assert expected_path in normalized_files, f"Expected file {expected_path} missing from BACKUP archive"
        assert normalized_files[expected_path] == expected_content, f"Content mismatch for {expected_path}"

    assert len(normalized_files) == len(expected_files), f"Archive contains unexpected files: {list(normalized_files.keys())}"

def test_history_command():
    raw_response = send_command("HISTORY\n")
    expected_json = b'[{"timestamp": 1600000000, "files": ["old.json"]}]'
    assert raw_response.strip() == expected_json, f"HISTORY command returned unexpected data: {raw_response!r}"

def test_frame_hash_command():
    # Calculate expected hash using ffmpeg
    try:
        cmd = [
            "ffmpeg", "-i", "/app/config_history.mp4", 
            "-vf", "select='eq(n\\,10)'", 
            "-vframes", "1", 
            "-f", "image2pipe", 
            "-vcodec", "ppm", "-"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        frame_data = result.stdout
        expected_hash = hashlib.sha256(frame_data).hexdigest()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to extract frame 10 locally to compute truth hash: {e.stderr.decode()}")

    raw_response = send_command("FRAME_HASH 10\n")
    actual_hash = raw_response.decode('utf-8').strip()

    assert actual_hash.lower() == expected_hash.lower(), f"FRAME_HASH 10 returned {actual_hash}, expected {expected_hash}"