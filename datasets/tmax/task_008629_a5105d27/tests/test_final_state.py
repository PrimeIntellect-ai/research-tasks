# test_final_state.py

import os
import subprocess
import pytest

def test_attacker_ip_file():
    ip_file = "/home/user/attacker_ip.txt"
    assert os.path.isfile(ip_file), f"File {ip_file} does not exist."

    with open(ip_file, "r") as f:
        ip = f.read().strip()

    # The expected IP is derived from the access log where the response is 200 for the SSH key
    assert ip == "172.16.5.99", f"Expected attacker IP to be '172.16.5.99', but got '{ip}'."

def test_binary_exists_and_executable():
    binary_path = "/home/user/service/uploader_fixed"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist. Did you compile it?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_normal_file_behavior():
    binary_path = "/home/user/service/uploader_fixed"
    try:
        result = subprocess.run(
            [binary_path, "normal.log"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Execution of uploader_fixed timed out.")

    assert result.returncode == 0, f"Expected normal file to return 0, got {result.returncode}."
    assert "Access Denied" not in result.stdout, "Normal file was incorrectly blocked with 'Access Denied'."

def test_path_traversal_prevention():
    binary_path = "/home/user/service/uploader_fixed"
    try:
        result = subprocess.run(
            [binary_path, "../.ssh/id_rsa"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Execution of uploader_fixed timed out.")

    assert result.returncode == 1, f"Expected path traversal attempt to return 1, got {result.returncode}."
    assert result.stdout.strip() == "Access Denied", f"Expected output to be exactly 'Access Denied', got '{result.stdout.strip()}'."