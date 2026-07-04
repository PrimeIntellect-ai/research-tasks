# test_final_state.py

import os
import io
import zipfile
import hashlib
import requests
import pytest
import csv

BASE_URL = "http://127.0.0.1:8000"
AUTH_HEADER = {"Authorization": "Bearer crimson skyline protocol"}
ARTIFACTS_DIR = "/home/user/artifacts"

def create_zip_in_memory(file_contents: dict) -> bytes:
    """Helper to create a zip file in memory from a dict of filename: content strings."""
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for filename, content in file_contents.items():
            zf.writestr(filename, content)
    return mem_zip.getvalue()

def get_sha256(content: str) -> str:
    """Helper to calculate SHA256 of a string."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def test_artifact_repository_sequence():
    """
    Executes the multi-protocol sequence to verify the artifact repository.
    This ensures the server handles authentication, prevents Zip Slip, 
    extracts files correctly, and maintains an accurate checksum manifest.
    """
    # Wait for server to be up (basic check)
    try:
        requests.get(BASE_URL)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to server at {BASE_URL}. Is it running?")

    # 1. No Auth -> 401
    safe_zip_bytes = create_zip_in_memory({"test.txt": "hello"})
    resp_no_auth = requests.post(
        f"{BASE_URL}/upload",
        files={"archive": ("safe.zip", safe_zip_bytes, "application/zip")}
    )
    assert resp_no_auth.status_code == 401, \
        f"Expected 401 Unauthorized when missing auth, got {resp_no_auth.status_code}. Response: {resp_no_auth.text}"

    # 2. Malicious ZIP + Auth -> 400 + Zip Slip error
    malicious_zip_bytes = create_zip_in_memory({"../../../home/user/hacked.txt": "hacked"})
    resp_malicious = requests.post(
        f"{BASE_URL}/upload",
        headers=AUTH_HEADER,
        files={"archive": ("malicious.zip", malicious_zip_bytes, "application/zip")}
    )
    assert resp_malicious.status_code == 400, \
        f"Expected 400 Bad Request for Zip Slip attempt, got {resp_malicious.status_code}. Response: {resp_malicious.text}"

    try:
        json_resp = resp_malicious.json()
        assert json_resp.get("error") == "Zip Slip detected", \
            f"Expected JSON error message 'Zip Slip detected', got {json_resp}"
    except ValueError:
        pytest.fail(f"Expected JSON response for Zip Slip error, got: {resp_malicious.text}")

    # Verify the malicious file was NOT extracted
    assert not os.path.exists("/home/user/artifacts/hacked.txt"), "Zip Slip failed: hacked.txt was extracted into artifacts dir."
    assert not os.path.exists("/home/user/hacked.txt"), "Zip Slip failed: hacked.txt was extracted outside artifacts dir."

    # 3. Safe ZIP v1 + Auth -> 200
    safe_v1_bytes = create_zip_in_memory({"config.json": "v1"})
    resp_v1 = requests.post(
        f"{BASE_URL}/upload",
        headers=AUTH_HEADER,
        files={"archive": ("safe_v1.zip", safe_v1_bytes, "application/zip")}
    )
    assert resp_v1.status_code == 200, \
        f"Expected 200 OK for safe v1 upload, got {resp_v1.status_code}. Response: {resp_v1.text}"

    # 4. GET manifest -> 200 + CSV with v1 hash
    resp_manifest_v1 = requests.get(f"{BASE_URL}/manifest", headers=AUTH_HEADER)
    assert resp_manifest_v1.status_code == 200, \
        f"Expected 200 OK for GET /manifest, got {resp_manifest_v1.status_code}. Response: {resp_manifest_v1.text}"

    manifest_v1_text = resp_manifest_v1.text
    reader_v1 = csv.DictReader(io.StringIO(manifest_v1_text))
    rows_v1 = list(reader_v1)

    assert reader_v1.fieldnames == ["filename", "sha256"], \
        f"Expected CSV header 'filename,sha256', got {reader_v1.fieldnames}"

    v1_hash = get_sha256("v1")
    config_row_v1 = next((row for row in rows_v1 if row["filename"] == "config.json"), None)
    assert config_row_v1 is not None, "config.json missing from manifest after v1 upload"
    assert config_row_v1["sha256"] == v1_hash, \
        f"Expected hash {v1_hash} for config.json, got {config_row_v1['sha256']}"

    # 5. Safe ZIP v2 + Auth -> 200
    safe_v2_bytes = create_zip_in_memory({"config.json": "v2", "data.xml": "<data/>"})
    resp_v2 = requests.post(
        f"{BASE_URL}/upload",
        headers=AUTH_HEADER,
        files={"archive": ("safe_v2.zip", safe_v2_bytes, "application/zip")}
    )
    assert resp_v2.status_code == 200, \
        f"Expected 200 OK for safe v2 upload, got {resp_v2.status_code}. Response: {resp_v2.text}"

    # 6. GET manifest -> 200 + CSV with v2 hashes
    resp_manifest_v2 = requests.get(f"{BASE_URL}/manifest", headers=AUTH_HEADER)
    assert resp_manifest_v2.status_code == 200, \
        f"Expected 200 OK for GET /manifest, got {resp_manifest_v2.status_code}. Response: {resp_manifest_v2.text}"

    manifest_v2_text = resp_manifest_v2.text
    reader_v2 = csv.DictReader(io.StringIO(manifest_v2_text))
    rows_v2 = list(reader_v2)

    v2_hash = get_sha256("v2")
    data_hash = get_sha256("<data/>")

    config_row_v2 = next((row for row in rows_v2 if row["filename"] == "config.json"), None)
    data_row_v2 = next((row for row in rows_v2 if row["filename"] == "data.xml"), None)

    assert config_row_v2 is not None, "config.json missing from manifest after v2 upload"
    assert config_row_v2["sha256"] == v2_hash, \
        f"Expected updated hash {v2_hash} for config.json, got {config_row_v2['sha256']}"

    assert data_row_v2 is not None, "data.xml missing from manifest after v2 upload"
    assert data_row_v2["sha256"] == data_hash, \
        f"Expected hash {data_hash} for data.xml, got {data_row_v2['sha256']}"