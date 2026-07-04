# test_final_state.py

import os
import pytest

def test_investigation_file_exists():
    """Verify that the investigation report was created."""
    file_path = "/home/user/investigation.txt"
    assert os.path.isfile(file_path), f"Expected investigation report not found at {file_path}"

def test_investigation_file_contents():
    """Verify the contents of the investigation report."""
    file_path = "/home/user/investigation.txt"
    with open(file_path, "r") as f:
        content = f.read()

    expected_ip = "Malicious Source IP: 203.0.113.88"
    expected_token = "Forged Token: 99999999999999999999999999999999"
    expected_c2 = "C2 Server: 198.51.100.99"

    assert expected_ip in content, f"Missing or incorrect Malicious Source IP in {file_path}"
    assert expected_token in content, f"Missing or incorrect Forged Token in {file_path}"
    assert expected_c2 in content, f"Missing or incorrect C2 Server in {file_path}"

def test_payload_bin_exists():
    """Verify that the extracted binary payload was saved."""
    file_path = "/home/user/payload.bin"
    assert os.path.isfile(file_path), f"Expected extracted binary not found at {file_path}"

def test_payload_bin_is_elf():
    """Verify that the extracted payload is an ELF binary."""
    file_path = "/home/user/payload.bin"
    with open(file_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File at {file_path} does not appear to be a valid ELF binary (incorrect magic bytes)."