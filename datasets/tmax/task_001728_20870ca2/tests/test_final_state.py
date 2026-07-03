# test_final_state.py

import os
import json
import hashlib
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer backup_token_2024"}
MEDIA_DIR = "/app/media_assets"

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_auth_required():
    """Test that endpoints require authentication."""
    try:
        response = requests.get(f"{BASE_URL}/manifest", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {BASE_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without auth header, got {response.status_code}"

def test_manifest_endpoint():
    """Test the /manifest endpoint returns correct JSON with expected hashes."""
    try:
        response = requests.get(f"{BASE_URL}/manifest", headers=AUTH_HEADER, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for /manifest, got {response.status_code}"

    try:
        manifest = response.json()
    except json.JSONDecodeError:
        pytest.fail("Response body from /manifest is not valid JSON.")

    expected_files = {
        "logs/system.log": os.path.join(MEDIA_DIR, "logs/system.log"),
        "documents/data.txt": os.path.join(MEDIA_DIR, "documents/data.txt"),
        "documents/external_link.txt": os.path.join(MEDIA_DIR, "documents/external_link.txt"),
        "surveillance.mp4": os.path.join(MEDIA_DIR, "surveillance.mp4")
    }

    for rel_path, abs_path in expected_files.items():
        assert rel_path in manifest, f"Expected file '{rel_path}' missing from manifest."
        expected_hash = compute_sha256(abs_path)
        assert manifest[rel_path] == expected_hash, f"Hash mismatch for '{rel_path}'. Expected {expected_hash}, got {manifest[rel_path]}"

def test_thumbnail_endpoint():
    """Test the /thumbnail endpoint returns a valid PNG image."""
    try:
        response = requests.get(f"{BASE_URL}/thumbnail", headers=AUTH_HEADER, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for /thumbnail, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "image/png" in content_type, f"Expected Content-Type 'image/png', got '{content_type}'"

    body = response.content
    assert len(body) > 8, "Response body is too short to be a valid PNG."

    # Check PNG magic bytes
    png_magic = b'\x89PNG\r\n\x1a\n'
    assert body.startswith(png_magic), "Response body does not start with PNG magic bytes."