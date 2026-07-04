# test_final_state.py

import os
import hashlib
import requests
import pytest

RELEASE_DIR = "/app/project_delta"
PORT = 8888
BASE_URL = f"http://127.0.0.1:{PORT}"

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def test_release_directory_exists():
    assert os.path.isdir(RELEASE_DIR), f"Directory {RELEASE_DIR} does not exist. Did you transcribe the audio correctly?"

def test_extracted_files_exist_and_renamed():
    alpha_path = os.path.join(RELEASE_DIR, "alpha.bin")
    beta_path = os.path.join(RELEASE_DIR, "beta.bin")

    assert os.path.isfile(alpha_path), f"{alpha_path} does not exist."
    assert os.path.isfile(beta_path), f"{beta_path} does not exist."

    assert os.path.getsize(alpha_path) == 100, f"{alpha_path} has incorrect size."
    assert os.path.getsize(beta_path) == 200, f"{beta_path} has incorrect size."

def test_latest_symlink():
    symlink_path = os.path.join(RELEASE_DIR, "latest.bin")
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    assert os.path.basename(target) == "beta.bin", f"{symlink_path} does not point to beta.bin (the largest file)."

def test_sha256sums_file():
    sums_path = os.path.join(RELEASE_DIR, "SHA256SUMS")
    assert os.path.isfile(sums_path), f"{sums_path} does not exist."

    alpha_path = os.path.join(RELEASE_DIR, "alpha.bin")
    beta_path = os.path.join(RELEASE_DIR, "beta.bin")

    expected_alpha_hash = get_sha256(alpha_path)
    expected_beta_hash = get_sha256(beta_path)

    with open(sums_path, 'r') as f:
        content = f.read()

    assert expected_alpha_hash in content, "SHA256SUMS is missing the hash for alpha.bin."
    assert expected_beta_hash in content, "SHA256SUMS is missing the hash for beta.bin."

def test_http_server_sha256sums():
    try:
        response = requests.get(f"{BASE_URL}/SHA256SUMS", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on port {PORT}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for /SHA256SUMS, got {response.status_code}"

    alpha_path = os.path.join(RELEASE_DIR, "alpha.bin")
    beta_path = os.path.join(RELEASE_DIR, "beta.bin")

    expected_alpha_hash = get_sha256(alpha_path)
    expected_beta_hash = get_sha256(beta_path)

    content = response.text
    assert expected_alpha_hash in content, "HTTP response for SHA256SUMS is missing the hash for alpha.bin."
    assert expected_beta_hash in content, "HTTP response for SHA256SUMS is missing the hash for beta.bin."

def test_http_server_latest_bin():
    try:
        response = requests.get(f"{BASE_URL}/latest.bin", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on port {PORT}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for /latest.bin, got {response.status_code}"
    assert len(response.content) == 200, f"Expected /latest.bin to serve 200 bytes, got {len(response.content)} bytes."