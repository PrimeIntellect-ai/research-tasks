# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error

def test_decrypted_log():
    """Verify that the decrypted.log file contains the expected plaintext."""
    log_path = "/home/user/investigation/decrypted.log"
    assert os.path.isfile(log_path), f"File not found: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    expected_lines = [
        "2024-05-10T12:00:00Z | exfil_success | IP: 192.168.1.55 | bytes: 1024",
        "2024-05-10T12:05:00Z | exfil_failed | IP: 10.0.0.1 | bytes: 0",
        "2024-05-10T12:10:00Z | exfil_success | IP: 203.0.113.42 | bytes: 5000",
        "2024-05-10T12:15:00Z | login_attempt | IP: 192.168.1.55 | bytes: 0",
        "2024-05-10T12:20:00Z | exfil_success | IP: 192.168.1.55 | bytes: 2048",
        "2024-05-10T12:25:00Z | exfil_success | IP: 198.51.100.7 | bytes: 128"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line missing from decrypted.log: {line}"

def test_attacker_ips():
    """Verify that attacker_ips.txt contains the correct unique IPs for exfil_success."""
    ips_path = "/home/user/investigation/attacker_ips.txt"
    assert os.path.isfile(ips_path), f"File not found: {ips_path}"

    with open(ips_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ips = ["192.168.1.55", "198.51.100.7", "203.0.113.42"]

    assert sorted(lines) == sorted(expected_ips), f"Expected IPs {expected_ips}, but got {lines}"

def test_server_patched_execution():
    """Verify that the patched server binary exists, runs, serves valid files, and blocks path traversal."""
    binary_path = "/home/user/investigation/server_patched"
    assert os.path.isfile(binary_path), f"File not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"File is not executable: {binary_path}"

    # Setup dummy environment for the server
    os.makedirs("/var/www/uploads", exist_ok=True)
    test_file_path = "/var/www/uploads/test_valid.txt"
    with open(test_file_path, "w") as f:
        f.write("VALID_CONTENT")

    # Start the patched server
    proc = subprocess.Popen([binary_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)  # Allow server to start

    try:
        # 1. Test valid request
        req = urllib.request.Request("http://127.0.0.1:8080/download?file=test_valid.txt")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200, "Valid request did not return 200 OK"
                body = response.read().decode()
                assert body == "VALID_CONTENT", "Valid request did not return correct file content"
        except urllib.error.URLError as e:
            assert False, f"Valid request failed completely: {e}"

        # 2. Test path traversal request
        req = urllib.request.Request("http://127.0.0.1:8080/download?file=../../../../etc/passwd")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status in [400, 403, 404], f"Path traversal succeeded with status {response.status}, expected 400, 403, or 404"
        except urllib.error.HTTPError as e:
            assert e.code in [400, 403, 404], f"Path traversal returned unexpected error code {e.code}, expected 400, 403, or 404"
        except urllib.error.URLError as e:
            assert False, f"Path traversal request failed to connect: {e}"

    finally:
        proc.terminate()
        proc.wait()
        if os.path.exists(test_file_path):
            os.remove(test_file_path)