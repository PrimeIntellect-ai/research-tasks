# test_final_state.py

import os
import io
import json
import tarfile
import zipfile
import subprocess
import tempfile
import requests
import pytest

SERVICE_URL = "http://127.0.0.1:9090/api/v1/process_archive"

def get_expected_hash(content_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(content_bytes)
        f.flush()
        temp_name = f.name
    try:
        res = subprocess.run(["/app/dedup_hash", temp_name], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    finally:
        os.remove(temp_name)

def test_service_running():
    """Check if the service is listening on the expected port."""
    try:
        # Just a basic connection check
        requests.get("http://127.0.0.1:9090/")
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not listening on 127.0.0.1:9090")
    except requests.exceptions.RequestException:
        pass # Expected since GET / might not be implemented

def test_process_complex_archive():
    """Test the service with a complex archive containing nested zip, encodings, and symlinks."""

    # 1. Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # Shift_JIS encoded text
        zf.writestr("inner.txt", "こんにちは".encode("shift_jis"))
    zip_data = zip_buffer.getvalue()

    # 2. Create a tar file in memory
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tf:
        # Add UTF-16LE text file
        utf16_content = "Storage Admin".encode("utf-16le")
        tinfo1 = tarfile.TarInfo("root_file.txt")
        tinfo1.size = len(utf16_content)
        tf.addfile(tinfo1, io.BytesIO(utf16_content))

        # Add the zip file
        tinfo2 = tarfile.TarInfo("archive.zip")
        tinfo2.size = len(zip_data)
        tf.addfile(tinfo2, io.BytesIO(zip_data))

        # Add a cyclic symlink
        tinfo3 = tarfile.TarInfo("bad_link")
        tinfo3.type = tarfile.SYMTYPE
        tinfo3.linkname = "."
        tf.addfile(tinfo3)

    tar_data = tar_buffer.getvalue()

    # 3. Send to service
    try:
        response = requests.post(SERVICE_URL, data=tar_data, headers={"Content-Type": "application/x-tar"}, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect or send request to service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Body: {response.text}"

    try:
        resp_json = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Body: {response.text}")

    assert "manifest" in resp_json, "Response JSON missing 'manifest' key."
    manifest = resp_json["manifest"]

    # 4. Verify expected hashes
    expected_root_hash = get_expected_hash("Storage Admin".encode("utf-8"))
    expected_inner_hash = get_expected_hash("こんにちは".encode("utf-8"))

    assert "root_file.txt" in manifest, "Missing 'root_file.txt' in manifest"
    assert manifest["root_file.txt"] == expected_root_hash, f"Hash mismatch for root_file.txt. Expected {expected_root_hash}, got {manifest['root_file.txt']}"

    assert "archive/inner.txt" in manifest, "Missing 'archive/inner.txt' in manifest"
    assert manifest["archive/inner.txt"] == expected_inner_hash, f"Hash mismatch for archive/inner.txt. Expected {expected_inner_hash}, got {manifest['archive/inner.txt']}"

    # Ensure no bad_link in manifest
    assert "bad_link" not in manifest, "Symlink 'bad_link' should not be processed or included in manifest."

def test_process_deep_nesting():
    """Test deep nesting of tar archives."""
    # inner.tar
    inner_tar_buf = io.BytesIO()
    with tarfile.open(fileobj=inner_tar_buf, mode="w") as tf:
        content = b"Deeply nested data"
        tinfo = tarfile.TarInfo("deep.bin")
        tinfo.size = len(content)
        tf.addfile(tinfo, io.BytesIO(content))
    inner_tar_data = inner_tar_buf.getvalue()

    # middle.tar
    middle_tar_buf = io.BytesIO()
    with tarfile.open(fileobj=middle_tar_buf, mode="w") as tf:
        tinfo = tarfile.TarInfo("inner.tar")
        tinfo.size = len(inner_tar_data)
        tf.addfile(tinfo, io.BytesIO(inner_tar_data))
    middle_tar_data = middle_tar_buf.getvalue()

    # outer.tar
    outer_tar_buf = io.BytesIO()
    with tarfile.open(fileobj=outer_tar_buf, mode="w") as tf:
        tinfo = tarfile.TarInfo("middle.tar")
        tinfo.size = len(middle_tar_data)
        tf.addfile(tinfo, io.BytesIO(middle_tar_data))
    outer_tar_data = outer_tar_buf.getvalue()

    try:
        response = requests.post(SERVICE_URL, data=outer_tar_data, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect or send request to service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Body: {response.text}"
    resp_json = response.json()
    manifest = resp_json.get("manifest", {})

    expected_hash = get_expected_hash(b"Deeply nested data")
    expected_path = "middle/inner/deep.bin"

    assert expected_path in manifest, f"Missing '{expected_path}' in manifest"
    assert manifest[expected_path] == expected_hash, "Hash mismatch for deeply nested file."