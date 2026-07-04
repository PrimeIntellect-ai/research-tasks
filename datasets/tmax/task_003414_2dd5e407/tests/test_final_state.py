# test_final_state.py

import os
import requests
import pytest

def test_chunks_created_correctly():
    """Verify that chunks are created for valid archives and not for corrupt ones."""
    chunks_dir = "/home/user/data/chunks"

    # Check chunks for app-v1.tar.gz
    app_chunks = sorted([f for f in os.listdir(chunks_dir) if f.startswith("app-v1.tar.gz.chunk.")])
    assert len(app_chunks) > 0, "No chunks found for app-v1.tar.gz"

    for i, chunk_file in enumerate(app_chunks):
        chunk_path = os.path.join(chunks_dir, chunk_file)
        size = os.path.getsize(chunk_path)
        if i < len(app_chunks) - 1:
            assert size == 512000, f"Chunk {chunk_file} has incorrect size: {size} (expected 512000)"
        else:
            assert size <= 512000, f"Last chunk {chunk_file} is too large: {size}"

    # Check that no chunks exist for corrupt-v2.tar.gz
    corrupt_chunks = [f for f in os.listdir(chunks_dir) if f.startswith("corrupt-v2.tar.gz")]
    assert len(corrupt_chunks) == 0, "Chunks found for corrupt-v2.tar.gz, but it should have been skipped."

def test_symlinks_created_correctly():
    """Verify that symlinks are created for valid archives and not for corrupt ones."""
    active_dir = "/home/user/data/active"
    app_symlink = os.path.join(active_dir, "app-v1.tar.gz")
    corrupt_symlink = os.path.join(active_dir, "corrupt-v2.tar.gz")

    assert os.path.islink(app_symlink), "Symlink for app-v1.tar.gz is missing."
    target = os.readlink(app_symlink)
    assert target == "/home/user/data/archives/app-v1.tar.gz", f"Symlink points to wrong target: {target}"

    assert not os.path.exists(corrupt_symlink) and not os.path.islink(corrupt_symlink), "Symlink found for corrupt-v2.tar.gz."

def test_api_health():
    """Verify the Nginx reverse proxy routes to the Rust HTTP server correctly."""
    url = "http://127.0.0.1:8080/api/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.text.strip() == "System Operational", f"Expected body 'System Operational', got '{response.text}'"

def test_downloads_valid_archive():
    """Verify Nginx serves the valid archive from the active directory."""
    url = "http://127.0.0.1:8080/downloads/app-v1.tar.gz"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    original_file = "/home/user/data/archives/app-v1.tar.gz"
    with open(original_file, "rb") as f:
        expected_content = f.read()

    assert response.content == expected_content, "Downloaded content does not match the original archive."

def test_downloads_corrupt_archive():
    """Verify Nginx returns 404 for the corrupt archive since no symlink should exist."""
    url = "http://127.0.0.1:8080/downloads/corrupt-v2.tar.gz"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 404, f"Expected status 404 for missing file, got {response.status_code}"