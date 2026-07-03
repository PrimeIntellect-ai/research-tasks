# test_final_state.py
import os
import io
import tarfile
import threading
import requests
import pytest
import time

BASE_URL = "http://127.0.0.1:8888"
UPLOAD_DIR = "/home/user/service_root/uploads"

def create_tar_archive(files):
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        for name, content in files.items():
            content_bytes = content.encode('utf-8')
            tarinfo = tarfile.TarInfo(name=name)
            tarinfo.size = len(content_bytes)
            tar.addfile(tarinfo, io.BytesIO(content_bytes))
    tar_stream.seek(0)
    return tar_stream.read()

def test_service_listening():
    """Verify that the service is running and listening on the correct port."""
    try:
        response = requests.get(f"{BASE_URL}/")
        # Just checking if connection is refused or not. 
        # The root might return 404, which is fine.
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not listening on 127.0.0.1:8888")

def test_safe_upload():
    """Verify that a safe tar archive is extracted correctly."""
    tar_data = create_tar_archive({"safe_file.txt": "safe content"})
    response = requests.post(f"{BASE_URL}/upload", data=tar_data)
    assert response.status_code in [200, 201, 204], f"Upload failed with status {response.status_code}"

    # Check if file exists via GET
    get_resp = requests.get(f"{BASE_URL}/files/safe_file.txt")
    assert get_resp.status_code == 200, "Failed to retrieve uploaded file via GET"
    assert get_resp.text == "safe content", "File content mismatch"

def test_zip_slip_vulnerability():
    """Verify that a malicious tar archive does not write outside the upload directory."""
    malicious_path = "../../../../../../../../../../../home/user/flag.txt"
    tar_data = create_tar_archive({malicious_path: "pwned"})

    # Remove the flag if it exists from previous runs
    flag_path = "/home/user/flag.txt"
    if os.path.exists(flag_path):
        os.remove(flag_path)

    try:
        requests.post(f"{BASE_URL}/upload", data=tar_data)
    except Exception:
        pass # The server might drop the connection, which is an acceptable way to reject

    assert not os.path.exists(flag_path), "Zip slip vulnerability exists! File was written outside UPLOAD_DIR."

def test_concurrency():
    """Verify that concurrent uploads do not corrupt each other."""
    num_threads = 5
    results = []

    def upload_task(i):
        tar_data = create_tar_archive({f"concurrent_{i}.txt": f"content_{i}"})
        try:
            resp = requests.post(f"{BASE_URL}/upload", data=tar_data)
            results.append((i, resp.status_code))
        except Exception as e:
            results.append((i, str(e)))

    threads = [threading.Thread(target=upload_task, args=(i,)) for i in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for i in range(num_threads):
        get_resp = requests.get(f"{BASE_URL}/files/concurrent_{i}.txt")
        assert get_resp.status_code == 200, f"Concurrent file {i} failed to upload or extract properly."
        assert get_resp.text == f"content_{i}", f"Concurrent file {i} content mismatch."

def test_install_directory():
    """Verify that the Makefile installed the application to the correct directory."""
    assert os.path.isdir("/home/user/service_root"), "Installation directory /home/user/service_root does not exist."
    assert os.path.isdir(UPLOAD_DIR), f"Upload directory {UPLOAD_DIR} does not exist."