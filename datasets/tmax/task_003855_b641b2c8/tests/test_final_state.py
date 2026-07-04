# test_final_state.py
import os
import io
import zipfile
import base64
import requests
import subprocess
import pytest

def get_hash(content: bytes) -> str:
    # Compute the djb2 hash exactly as the C program does
    hash_val = 5381
    for b in content:
        hash_val = ((hash_val << 5) + hash_val) + b
        hash_val &= 0xFFFFFFFFFFFFFFFF # Keep it within 64-bit unsigned just in case, though python handles large ints
    # The C program uses unsigned long, which is typically 64-bit on x86_64 Linux.
    # We can just call the binary to be absolutely sure.
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(content)
        tmp_name = tmp.name

    try:
        result = subprocess.run(["/app/config_hasher", tmp_name], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    finally:
        os.remove(tmp_name)

def test_process_config_endpoint():
    # 1. Prepare the initial zip file
    wal_content = (
        "APPEND|core.conf|cG9ydD05MDkw\n"
        "CREATE|new.json|eyJrZXkiOiAidmFsIn0=\n"
        "DELETE|old.txt|none\n"
    )

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        zf.writestr("core.conf", "server=1\n")
        zf.writestr("old.txt", "delete me")
        zf.writestr("update.wal", wal_content)

    zip_bytes = zip_buffer.getvalue()

    # 2. Send the request
    url = "http://127.0.0.1:8000/process_config"
    try:
        response = requests.post(url, data=zip_bytes, headers={"Content-Type": "application/zip"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to or read from {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text[:200]}"

    # 3. Parse the response zip
    resp_zip_buffer = io.BytesIO(response.content)
    try:
        with zipfile.ZipFile(resp_zip_buffer, 'r') as zf:
            files = zf.namelist()

            # Assert update.wal is missing
            assert "update.wal" not in files, "update.wal should have been deleted from the final archive"

            # Assert files exist
            assert "core.conf" in files, "core.conf is missing from the response"
            assert "new.json" in files, "new.json is missing from the response"
            assert "old.txt" not in files, "old.txt should have been deleted"
            assert "hashes.txt" in files, "hashes.txt is missing from the response"

            # Assert file contents
            core_conf = zf.read("core.conf")
            assert core_conf == b"server=1\nport=9090", f"Unexpected core.conf content: {core_conf}"

            new_json = zf.read("new.json")
            assert new_json == b'{"key": "val"}', f"Unexpected new.json content: {new_json}"

            # Assert hashes.txt contents
            hashes_txt = zf.read("hashes.txt").decode('utf-8').strip().split('\n')

            expected_core_hash = get_hash(b"server=1\nport=9090")
            expected_new_hash = get_hash(b'{"key": "val"}')

            expected_lines = [
                f"core.conf: {expected_core_hash}",
                f"new.json: {expected_new_hash}"
            ]

            assert sorted(hashes_txt) == sorted(expected_lines), f"hashes.txt contents mismatch. Got: {hashes_txt}, Expected: {expected_lines}"

    except zipfile.BadZipFile:
        pytest.fail("Response body is not a valid ZIP archive")