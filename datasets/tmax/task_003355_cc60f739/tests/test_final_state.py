# test_final_state.py

import os
import json
import time
import zipfile
import shutil
import pytest
import requests

def create_malicious_zip(zip_path):
    # Create a zip file with a manifest.json, content/intro.md, and a malicious path
    manifest = [
        {
            "source": "content/intro.md",
            "published_path": "manual/intro.md",
            "version": "v3.14"
        }
    ]

    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr('manifest.json', json.dumps(manifest))
        zf.writestr('content/intro.md', '# Introduction\n\nVersion: __VERSION__\n')
        # Malicious entry
        zf.writestr('../../home/user/canary.txt', 'You have been hacked!')

@pytest.fixture(scope="module", autouse=True)
def trigger_processing():
    zip_path = "/home/user/incoming/docs.zip"
    create_malicious_zip(zip_path)

    # Wait for the service to process the zip file
    timeout = 15
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not os.path.exists(zip_path):
            break
        time.sleep(1)

    # Extra sleep to ensure processing (extraction, transformation, symlinking) is complete
    time.sleep(2)

def test_zip_slip_mitigated():
    canary_path = "/home/user/canary.txt"
    assert not os.path.exists(canary_path), "Zip Slip vulnerability still present: canary file was extracted outside the destination directory."

def test_zip_file_deleted():
    zip_path = "/home/user/incoming/docs.zip"
    assert not os.path.exists(zip_path), f"Zip file {zip_path} was not deleted after processing."

def test_http_server_serves_transformed_content():
    url = "http://127.0.0.1:8080/docs/manual/intro.md"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    content = response.text
    assert "Version: v3.14" in content, "The markdown content was not properly transformed. Expected 'Version: v3.14' to be present."
    assert "__VERSION__" not in content, "The literal string '__VERSION__' was not replaced in the markdown content."

def test_symlink_created_correctly():
    symlink_path = "/home/user/www/manual/intro.md"
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."

    target_path = os.readlink(symlink_path)
    expected_target_suffix = "content/intro.md"
    assert target_path.endswith(expected_target_suffix), f"Symlink target {target_path} does not point to the expected extracted file."