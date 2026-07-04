# test_final_state.py

import os
import pytest

EXPECTED_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILz9m/3/RkF+wY1c7E+6x3FpZ9uE1iQ1+X1hU2+dummy fake@key"
EXPECTED_OPTIONS = 'command="/home/user/isolate.sh",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty'

def test_found_key_pub_extracted():
    found_key_path = "/home/user/found_key.pub"
    assert os.path.isfile(found_key_path), f"File {found_key_path} does not exist. Did you extract the section?"

    with open(found_key_path, "rb") as f:
        content = f.read()

    # The extracted section might contain a null terminator since it was a C-string
    content_str = content.decode('utf-8', errors='ignore').strip('\x00').strip()
    assert EXPECTED_KEY in content_str, f"{found_key_path} does not contain the expected SSH key. Found: {content_str}"

def test_authorized_keys_hardened():
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"File {auth_keys_path} does not exist."

    with open(auth_keys_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_entry = f"{EXPECTED_OPTIONS} {EXPECTED_KEY}"

    found = any(expected_entry in line for line in lines)
    assert found, f"The expected hardened SSH key entry was not found in {auth_keys_path}. Ensure the options are prepended exactly as requested."

def test_elf_offset_result():
    offset_file_path = "/home/user/elf_offset.txt"
    assert os.path.isfile(offset_file_path), f"File {offset_file_path} does not exist. Did you run your scanner?"

    with open(offset_file_path, "r") as f:
        content = f.read().strip()

    assert content == "1842", f"The offset written to {offset_file_path} is incorrect. Expected '1842', got '{content}'."

def test_scanner_cpp_exists():
    scanner_path = "/home/user/scanner.cpp"
    assert os.path.isfile(scanner_path), f"File {scanner_path} does not exist. You must write the C++ scanner program."

    with open(scanner_path, "r") as f:
        content = f.read()

    assert len(content.strip()) > 0, f"{scanner_path} is empty."
    assert "main" in content, f"{scanner_path} does not appear to be a valid C++ program (no main function found)."