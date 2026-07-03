# test_final_state.py
import os
import json
import zipfile
import io
import requests
import time
import pytest

URL = "http://127.0.0.1:9000/upload"

def wait_for_service():
    """Wait for the service to be available."""
    for _ in range(30):
        try:
            # We just test if the port is open by sending a GET (even if it returns 405/404)
            # or just let the first POST handle it.
            requests.get("http://127.0.0.1:9000/")
            return
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    pytest.fail("Service did not start on 127.0.0.1:9000")

def create_wal_content(sensor_id: str) -> bytes:
    """Create the binary content for a .wal file."""
    # 8 bytes magic + 16 bytes sensor ID (null padded)
    magic = b"WALMAGIC"
    padded_id = sensor_id.encode('utf-8').ljust(16, b'\x00')
    return magic + padded_id

def test_valid_zip_upload():
    wait_for_service()

    # Create a valid zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("reading.wal", create_wal_content("SENS_A"))
        zf.writestr("metrics.wal", create_wal_content("SENS_B"))
        # Add a non-wal file to ensure it's ignored
        zf.writestr("ignore.txt", b"Should be ignored")

    zip_bytes = zip_buffer.getvalue()

    response = requests.post(URL, data=zip_bytes, headers={"Content-Type": "application/zip"})

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Body: {response.text}"

    try:
        result = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(result, list), "Response JSON must be an array"

    expected = {"SENS_A_reading.wal", "SENS_B_metrics.wal"}
    actual = set(result)
    assert actual == expected, f"Expected {expected}, got {actual}"

def test_malicious_zip_upload():
    wait_for_service()

    # Ensure the target malicious path does not exist before the test
    malicious_path = "/tmp/hacked.wal"
    if os.path.exists(malicious_path):
        os.remove(malicious_path)

    # Create a malicious zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("normal.wal", create_wal_content("SENS_C"))
        # Add a file with a path traversal payload
        zf.writestr("../../../../tmp/hacked.wal", create_wal_content("SENS_X"))

    zip_bytes = zip_buffer.getvalue()

    response = requests.post(URL, data=zip_bytes, headers={"Content-Type": "application/zip"})

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Body: {response.text}"

    try:
        result = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(result, list), "Response JSON must be an array"

    expected = {"SENS_C_normal.wal"}
    actual = set(result)
    assert actual == expected, f"Expected {expected}, got {actual}. The service must ignore files with path traversal."

    # Verify that the malicious file was NOT extracted to /tmp/hacked.wal
    assert not os.path.exists(malicious_path), f"Zip slip vulnerability detected! {malicious_path} was created."