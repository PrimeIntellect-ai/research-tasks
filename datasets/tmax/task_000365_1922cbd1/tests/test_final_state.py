# test_final_state.py

import os
import tarfile
import requests
import pytest
import time

PORT = 8192
BASE_URL = f"http://127.0.0.1:{PORT}"

def wait_for_service():
    """Wait for the service to be up."""
    for _ in range(10):
        try:
            response = requests.get(f"{BASE_URL}/api/status", timeout=1)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False

def test_api_status():
    """Test the GET /api/status endpoint."""
    assert wait_for_service(), f"Service is not listening on port {PORT} or did not respond in time."

    response = requests.get(f"{BASE_URL}/api/status", timeout=5)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = {"port": 8192, "quota": 150, "status": "running"}
    assert data == expected_data, f"Expected JSON {expected_data}, got {data}"

def test_api_backup():
    """Test the POST /api/backup endpoint and verify the archive."""
    assert wait_for_service(), f"Service is not listening on port {PORT} or did not respond in time."

    # Remove archive if it exists from previous manual runs
    archive_path = "/app/backup/archive.tar.gz"
    if os.path.exists(archive_path):
        os.remove(archive_path)

    response = requests.post(f"{BASE_URL}/api/backup", timeout=15)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data == {"status": "success"}, f"Expected JSON {{'status': 'success'}}, got {data}"

    # Verify the backup file
    assert os.path.exists(archive_path), f"Backup archive {archive_path} was not created."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # The archive should contain the files from /app/storage/
        # They might be stored as 'storage/file1.dat', 'app/storage/file1.dat', or 'file1.dat'
        # Just check that the file names are present in the archive
        base_names = [os.path.basename(name) for name in names]
        assert "file1.dat" in base_names, "file1.dat is missing from the backup archive."
        assert "file2.dat" in base_names, "file2.dat is missing from the backup archive."