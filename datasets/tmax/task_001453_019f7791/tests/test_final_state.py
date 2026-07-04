# test_final_state.py

import os
import tarfile
import io
import time
import urllib.request
import subprocess
import pytest

def test_backup_system():
    # Wait for the service to be ready
    service_url = "http://localhost:8080/upload"

    # Generate identical 10MB contents for deduplication testing
    file_a_content = os.urandom(10 * 1024 * 1024)
    file_b_content = os.urandom(10 * 1024 * 1024)
    hacked_content = b"hacked_content_test"

    # We will send 5 archives
    for i in range(5):
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode='w:gz') as tar:
            # Add file A
            info_a = tarfile.TarInfo(name="A")
            info_a.size = len(file_a_content)
            tar.addfile(info_a, io.BytesIO(file_a_content))

            # Add file B
            info_b = tarfile.TarInfo(name="B")
            info_b.size = len(file_b_content)
            tar.addfile(info_b, io.BytesIO(file_b_content))

            # Add path traversal attempt in the first archive
            if i == 0:
                info_hacked = tarfile.TarInfo(name="../../../home/user/hacked.txt")
                info_hacked.size = len(hacked_content)
                tar.addfile(info_hacked, io.BytesIO(hacked_content))

        buf.seek(0)
        file_data = buf.read()

        # Build multipart/form-data request manually to avoid third-party dependencies like requests
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="backup_{i}.tar.gz"\r\n'
            f'Content-Type: application/gzip\r\n\r\n'
        ).encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

        req = urllib.request.Request(service_url, data=body)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        req.add_header('Content-Length', str(len(body)))

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                assert response.status == 200, f"Expected status 200, got {response.status}"
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to upload archive {i} to {service_url}. Error: {e}. Is Nginx and the Flask app running and accepting large files?")

    # 1. Verify Path Traversal Neutralization
    assert not os.path.exists("/home/user/hacked.txt"), "Security Vulnerability: Path traversal allowed writing to /home/user/hacked.txt"

    # 2. Verify Deduplication Ratio
    def get_size(logical=False):
        cmd = ["du", "-sb"]
        if logical: 
            cmd.append("-l")
        cmd.append("/home/user/backups")
        try:
            res = subprocess.check_output(cmd).decode().split()[0]
            return float(res)
        except Exception as e:
            pytest.fail(f"Failed to calculate directory size: {e}")

    physical_size = get_size(logical=False)
    logical_size = get_size(logical=True)

    ratio = logical_size / physical_size if physical_size > 0 else 0

    assert ratio >= 3.0, f"Deduplication ratio metric failed. Expected >= 3.0, got {ratio:.2f} (Logical: {logical_size}, Physical: {physical_size})"