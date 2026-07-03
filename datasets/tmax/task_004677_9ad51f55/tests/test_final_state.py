# test_final_state.py
import os
import io
import time
import zipfile
import requests
import concurrent.futures
import pytest

PORT = 8555
TOKEN = "ALPHA-99-BETA"
URL = f"http://127.0.0.1:{PORT}/analyze"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
SAFE_STORAGE = "/app/safe_storage"

def create_zip_slip():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        zf.writestr('../../../../../tmp/evil.txt', b'evil content')
    return buf.getvalue()

def create_valid_zip(prefix=""):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        zf.writestr(f'{prefix}test.txt', b'hello world')
        zf.writestr(f'{prefix}image.png', b'\x89PNG\r\n\x1a\nfake png')
        zf.writestr(f'{prefix}binary.bin', b'\x7fELF\x01\x01\x01fake elf')
    return buf.getvalue()

def test_unauthenticated_request():
    """Test that requests without the correct authorization header are rejected with 401."""
    try:
        response = requests.post(URL, data=b"dummy", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}. Response: {response.text}"

def test_zip_slip_rejection():
    """Test that an archive containing directory traversal attempts is rejected with 400."""
    payload = create_zip_slip()
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 for zip slip payload, got {response.status_code}. Response: {response.text}"

def test_valid_extraction_and_elf_deletion():
    """Test that a valid archive is extracted, ELF files are deleted, and others are retained."""
    payload = create_valid_zip(prefix="run1_")
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid payload, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got invalid JSON: {response.text}")

    assert "retained_files" in data, f"Response JSON missing 'retained_files' key: {data}"

    # Check file system
    assert os.path.exists(os.path.join(SAFE_STORAGE, "run1_test.txt")), "Text file was not extracted or was incorrectly deleted."
    assert os.path.exists(os.path.join(SAFE_STORAGE, "run1_image.png")), "PNG file was not extracted or was incorrectly deleted."
    assert not os.path.exists(os.path.join(SAFE_STORAGE, "run1_binary.bin")), "ELF file was extracted but not deleted as required."

def test_concurrent_requests():
    """Test that concurrent requests are handled safely (using file locking) without crashing."""
    num_requests = 5
    payloads = [create_valid_zip(prefix=f"concurrent_{i}_") for i in range(num_requests)]

    def send_request(payload):
        return requests.post(URL, headers=HEADERS, data=payload, timeout=10)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request, p) for p in payloads]
        responses = [f.result() for f in concurrent.futures.as_completed(futures)]

    for i, resp in enumerate(responses):
        assert resp.status_code == 200, f"Concurrent request failed with status {resp.status_code}. Response: {resp.text}"
        try:
            data = resp.json()
            assert "retained_files" in data, f"Response JSON missing 'retained_files' key: {data}"
        except ValueError:
            pytest.fail(f"Expected JSON response in concurrent request, got invalid JSON: {resp.text}")

    # Verify that all non-ELF files from concurrent requests were retained
    for i in range(num_requests):
        assert os.path.exists(os.path.join(SAFE_STORAGE, f"concurrent_{i}_test.txt")), f"Concurrent text file {i} missing."
        assert os.path.exists(os.path.join(SAFE_STORAGE, f"concurrent_{i}_image.png")), f"Concurrent PNG file {i} missing."
        assert not os.path.exists(os.path.join(SAFE_STORAGE, f"concurrent_{i}_binary.bin")), f"Concurrent ELF file {i} not deleted."