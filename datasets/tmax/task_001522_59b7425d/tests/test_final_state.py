# test_final_state.py

import os
import io
import zipfile
import requests
import pytest
import stat

def test_backup_service():
    # 1. Construct the ZIP payload in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        zf.writestr('docs/readme.txt', b"Hello World")
        zf.writestr('docs/copy.txt', b"Hello World")
        zf.writestr('images/logo.png', b"Fake PNG bytes")
        zf.writestr('../../home/user/evil.sh', b"echo Pwned")

    zip_buffer.seek(0)

    # 2. Send POST request to the server
    url = "http://127.0.0.1:9000/upload"
    files = {'archive': ('test.zip', zip_buffer, 'application/zip')}

    try:
        response = requests.post(url, files=files, timeout=5)
        # We don't strictly assert response status code as long as it works, 
        # but typically it should be 2xx.
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to or receive response from the server at {url}: {e}")

    # 3. Verification checks
    evil_path = "/home/user/evil.sh"
    assert not os.path.exists(evil_path), f"Zip slip prevention failed: {evil_path} should not exist."

    readme_path = "/home/user/backup_vault/docs/VAULTX_readme.txt"
    copy_path = "/home/user/backup_vault/docs/VAULTX_copy.txt"
    logo_path = "/home/user/backup_vault/images/VAULTX_logo.png"

    assert os.path.isfile(readme_path), f"Expected extracted file not found: {readme_path}"
    with open(readme_path, "r") as f:
        assert f.read() == "Hello World", f"Content mismatch in {readme_path}"

    assert os.path.isfile(copy_path), f"Expected extracted file not found: {copy_path}"
    with open(copy_path, "r") as f:
        assert f.read() == "Hello World", f"Content mismatch in {copy_path}"

    assert os.path.isfile(logo_path), f"Expected extracted file not found: {logo_path}"
    with open(logo_path, "r") as f:
        assert f.read() == "Fake PNG bytes", f"Content mismatch in {logo_path}"

    # Check hard link
    stat_readme = os.stat(readme_path)
    stat_copy = os.stat(copy_path)

    assert stat_readme.st_ino == stat_copy.st_ino, "Deduplication failed: copy.txt is not a hard link to readme.txt (inodes differ)."