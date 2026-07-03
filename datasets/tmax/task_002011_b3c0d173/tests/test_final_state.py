# test_final_state.py

import os
import socket
import pytest

def get_redis_value(key: str) -> str:
    """Helper to get a value from Redis using a raw socket."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect(('127.0.0.1', 6379))
        key_b = key.encode('utf-8')
        req = b"*2\r\n$3\r\nGET\r\n$" + str(len(key_b)).encode('utf-8') + b"\r\n" + key_b + b"\r\n"
        s.sendall(req)

        resp = b""
        while b"\r\n" not in resp:
            chunk = s.recv(1)
            if not chunk:
                break
            resp += chunk

        if resp.startswith(b"$-1"):
            return None

        if resp.startswith(b"$"):
            length = int(resp[1:-2])
            data = b""
            while len(data) < length + 2:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
            return data[:length].decode('utf-8')
        return None

def test_archive_size():
    """Check that the total size of files in /home/user/archives/ is <= 1.5 MB."""
    archive_dir = '/home/user/archives/'
    assert os.path.exists(archive_dir), f"{archive_dir} does not exist."

    total_size = 0
    for root, _, files in os.walk(archive_dir):
        for f in files:
            total_size += os.path.getsize(os.path.join(root, f))

    threshold = 1500000
    assert total_size > 0, "Archive directory is empty; no archives were created."
    assert total_size <= threshold, f"Archive size {total_size} bytes exceeds threshold of {threshold} bytes."

def test_no_raw_logs_remaining():
    """Ensure no unprocessed .log files remain in /home/user/raw_logs/."""
    raw_logs_dir = '/home/user/raw_logs/'
    assert os.path.exists(raw_logs_dir), f"{raw_logs_dir} does not exist."

    log_files = []
    for root, _, files in os.walk(raw_logs_dir):
        for f in files:
            if f.endswith('.log'):
                log_files.append(os.path.join(root, f))

    assert len(log_files) == 0, f"Found {len(log_files)} unprocessed .log files in {raw_logs_dir}, expected 0."

def test_redis_entries_for_done_files():
    """Ensure every .done file has a corresponding '1' entry in Redis under its original .log path."""
    raw_logs_dir = '/home/user/raw_logs/'
    assert os.path.exists(raw_logs_dir), f"{raw_logs_dir} does not exist."

    done_files = []
    for root, _, files in os.walk(raw_logs_dir):
        for f in files:
            if f.endswith('.log.done'):
                done_files.append(os.path.join(root, f))

    assert len(done_files) > 0, "No .log.done files found; script did not process and rename any files."

    for df in done_files:
        original_path = df[:-5]  # Strip '.done' to get the original '.log' path
        key = f"processed:{original_path}"
        val = get_redis_value(key)
        assert val == "1", f"Expected Redis key '{key}' to be '1', but got '{val}'."