# test_final_state.py

import os
import glob
import requests
import pytest

def test_unpacked_directory_state():
    """Verify that /app/unpacked contains exactly 54 files, no archives, and all extensions are lowercase."""
    unpacked_dir = "/app/unpacked"
    assert os.path.isdir(unpacked_dir), f"Directory {unpacked_dir} does not exist"

    all_files = []
    for root, _, files in os.walk(unpacked_dir):
        for file in files:
            all_files.append(os.path.join(root, file))

    assert len(all_files) == 54, f"Expected 54 files in {unpacked_dir}, found {len(all_files)}"

    for file_path in all_files:
        _, ext = os.path.splitext(file_path)
        if ext:
            assert ext == ext.lower(), f"File extension is not lowercase: {file_path}"
            assert ext not in ['.tar', '.gz', '.zip', '.tgz'], f"Found intermediate archive file: {file_path}"

def test_audio_links_directory_state():
    """Verify that /app/audio_links contains exactly 12 symlinks to .wav files."""
    audio_links_dir = "/app/audio_links"
    assert os.path.isdir(audio_links_dir), f"Directory {audio_links_dir} does not exist"

    links = os.listdir(audio_links_dir)
    assert len(links) == 12, f"Expected 12 links in {audio_links_dir}, found {len(links)}"

    for link in links:
        link_path = os.path.join(audio_links_dir, link)
        assert os.path.islink(link_path), f"Not a symlink: {link_path}"
        target = os.readlink(link_path)
        assert target.endswith('.wav'), f"Symlink target does not end with .wav: {target}"
        assert os.path.exists(link_path), f"Broken symlink: {link_path} -> {target}"

def test_service_stats_endpoint():
    """Verify GET /stats returns the correct counts."""
    url = "http://127.0.0.1:8080/stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "files_count" in data, "Response missing 'files_count'"
    assert "audio_links_count" in data, "Response missing 'audio_links_count'"

    assert data["files_count"] == 54, f"Expected files_count 54, got {data['files_count']}"
    assert data["audio_links_count"] == 12, f"Expected audio_links_count 12, got {data['audio_links_count']}"

def test_service_unlock_endpoint_success():
    """Verify POST /unlock with correct passphrase returns 200 OK."""
    url = "http://127.0.0.1:8080/unlock"
    payload = {"passphrase": "storage vault alpha"}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert data.get("status") == "unlocked", f"Expected status 'unlocked', got {data.get('status')}"

def test_service_unlock_endpoint_failure():
    """Verify POST /unlock with incorrect passphrase returns 403 Forbidden."""
    url = "http://127.0.0.1:8080/unlock"
    payload = {"passphrase": "wrong"}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}"