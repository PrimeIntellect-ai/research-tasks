# test_final_state.py
import os
import json
import struct
import hashlib
import requests
import pytest
import subprocess

def parse_archive(archive_path):
    files = {}
    with open(archive_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"DCAR", "Invalid archive magic"
        while True:
            file_id_bytes = f.read(2)
            if not file_id_bytes:
                break
            file_id = struct.unpack(">H", file_id_bytes)[0]
            file_size = struct.unpack(">I", f.read(4))[0]
            path_padded = f.read(128)
            path = path_padded.rstrip(b'\x00').decode('ascii')
            data = f.read(file_size)
            files[str(file_id)] = {
                "path": path,
                "data": data
            }
    return files

def get_legacy_info(file_path):
    result = subprocess.run(["/app/doc_indexer", file_path], capture_output=True, text=True)
    out = result.stdout.strip()
    return out.split(":", 1)

@pytest.fixture(scope="module")
def truth_data():
    archive_path = "/home/user/legacy_docs.dcar"
    assert os.path.exists(archive_path), "Archive missing"
    return parse_archive(archive_path)

def test_extracted_files(truth_data):
    base_dir = "/home/user/extracted_docs"
    for file_id, info in truth_data.items():
        expected_path = os.path.join(base_dir, info["path"])
        assert os.path.exists(expected_path), f"Extracted file missing: {expected_path}"
        with open(expected_path, "rb") as f:
            content = f.read()
        assert content == info["data"], f"Content mismatch for {expected_path}"

def test_manifest_json(truth_data):
    manifest_path = "/home/user/manifest.json"
    assert os.path.exists(manifest_path), f"Manifest file missing: {manifest_path}"
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    base_dir = "/home/user/extracted_docs"
    for file_id, info in truth_data.items():
        assert file_id in manifest, f"File ID {file_id} missing from manifest"
        entry = manifest[file_id]
        assert entry["path"] == info["path"], f"Path mismatch for File ID {file_id}"

        expected_md5 = hashlib.md5(info["data"]).hexdigest()
        assert entry["md5"] == expected_md5, f"MD5 mismatch for File ID {file_id}"

        extracted_path = os.path.join(base_dir, info["path"])
        legacy_hash, doc_type = get_legacy_info(extracted_path)
        assert entry["legacy_hash"] == legacy_hash, f"Legacy hash mismatch for File ID {file_id}"
        assert entry["doc_type"] == doc_type, f"Doc type mismatch for File ID {file_id}"

def test_http_server_auth():
    url = "http://127.0.0.1:8080/manifest"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP server is not reachable at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without auth, got {response.status_code}"

def test_http_server_manifest(truth_data):
    url = "http://127.0.0.1:8080/manifest"
    headers = {"Authorization": "Bearer secret-doc-token"}
    response = requests.get(url, headers=headers, timeout=2)

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected application/json Content-Type"

    manifest = response.json()
    for file_id in truth_data:
        assert file_id in manifest, f"File ID {file_id} missing from served manifest"

def test_http_server_docs(truth_data):
    headers = {"Authorization": "Bearer secret-doc-token"}
    for file_id, info in truth_data.items():
        url = f"http://127.0.0.1:8080/doc/{file_id}"
        response = requests.get(url, headers=headers, timeout=2)

        assert response.status_code == 200, f"Expected 200 OK for {url}, got {response.status_code}"
        assert "application/octet-stream" in response.headers.get("Content-Type", ""), "Expected application/octet-stream Content-Type"
        assert response.content == info["data"], f"Served content mismatch for File ID {file_id}"

def test_http_server_doc_not_found():
    headers = {"Authorization": "Bearer secret-doc-token"}
    url = "http://127.0.0.1:8080/doc/9999"
    response = requests.get(url, headers=headers, timeout=2)
    assert response.status_code == 404, f"Expected 404 Not Found for non-existent file, got {response.status_code}"