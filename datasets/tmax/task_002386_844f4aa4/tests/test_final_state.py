# test_final_state.py

import os
import fcntl
import pytest
import requests

def test_header_extracted():
    header_path = "/home/user/header.bin"
    assert os.path.isfile(header_path), f"Header file {header_path} is missing."
    with open(header_path, "rb") as f:
        content = f.read()
    assert len(content) == 32, f"Expected 32 bytes in header, got {len(content)}."
    assert content == b"A" * 32, "Header content does not match the first 32 bytes of dump.bin."

def test_chunks_created():
    chunks_dir = "/home/user/chunks"
    assert os.path.isdir(chunks_dir), f"Directory {chunks_dir} is missing."

    chunk_0 = os.path.join(chunks_dir, "chunk_0.bin")
    chunk_1 = os.path.join(chunks_dir, "chunk_1.bin")
    chunk_2 = os.path.join(chunks_dir, "chunk_2.bin")

    assert os.path.isfile(chunk_0), f"Chunk {chunk_0} is missing."
    assert os.path.getsize(chunk_0) == 1048576, f"Chunk 0 size incorrect."

    assert os.path.isfile(chunk_1), f"Chunk {chunk_1} is missing."
    assert os.path.getsize(chunk_1) == 1048576, f"Chunk 1 size incorrect."

    assert os.path.isfile(chunk_2), f"Chunk {chunk_2} is missing."
    assert os.path.getsize(chunk_2) == 500, f"Chunk 2 size incorrect."

def test_symlinks_created():
    links_dir = "/home/user/active_links"
    assert os.path.isdir(links_dir), f"Directory {links_dir} is missing."

    for i in range(3):
        link_path = os.path.join(links_dir, f"link_{i}.bin")
        target_path = f"/home/user/chunks/chunk_{i}.bin"

        assert os.path.islink(link_path), f"{link_path} is not a symlink."
        assert os.readlink(link_path) == target_path, f"Symlink {link_path} points to {os.readlink(link_path)} instead of {target_path}."

def test_server_lock():
    lock_path = "/home/user/server.lock"
    assert os.path.isfile(lock_path), f"Lock file {lock_path} does not exist."

    with open(lock_path, "w") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # If we succeed, the server is NOT holding the lock
            fcntl.flock(f, fcntl.LOCK_UN)
            pytest.fail("The server is not holding an exclusive lock on /home/user/server.lock.")
        except BlockingIOError:
            # Expected behavior: the lock is held by the server
            pass

def test_http_volume():
    url = "http://127.0.0.1:8888/volume"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."
    assert response.text.strip() == "CRITICAL_VOL_8841", f"Expected 'CRITICAL_VOL_8841', got '{response.text}'."

def test_http_chunks():
    base_url = "http://127.0.0.1:8888/chunk"

    # Test chunk 0
    try:
        resp_0 = requests.get(f"{base_url}/0", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server for chunk 0: {e}")

    assert resp_0.status_code == 200, f"Expected status code 200 for chunk 0, got {resp_0.status_code}."
    assert len(resp_0.content) == 1048576, f"Expected 1048576 bytes for chunk 0, got {len(resp_0.content)}."
    assert resp_0.content == b"B" * 1048576, "Content of chunk 0 via HTTP does not match expected."

    # Test chunk 2
    try:
        resp_2 = requests.get(f"{base_url}/2", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server for chunk 2: {e}")

    assert resp_2.status_code == 200, f"Expected status code 200 for chunk 2, got {resp_2.status_code}."
    assert len(resp_2.content) == 500, f"Expected 500 bytes for chunk 2, got {len(resp_2.content)}."
    assert resp_2.content == b"D" * 500, "Content of chunk 2 via HTTP does not match expected."