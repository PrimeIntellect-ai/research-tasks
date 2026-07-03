# test_final_state.py

import os
import pytest

def test_tampered_file_identified():
    tampered_file_path = "/home/user/tampered_file.txt"
    assert os.path.isfile(tampered_file_path), f"File {tampered_file_path} is missing."

    with open(tampered_file_path, "r") as f:
        content = f.read().strip()

    assert content == "sysctl.conf", f"Expected 'sysctl.conf' in {tampered_file_path}, but found '{content}'."

def test_recover_cpp_exists():
    recover_cpp_path = "/home/user/recover.cpp"
    assert os.path.isfile(recover_cpp_path), f"C++ source file {recover_cpp_path} is missing."

def test_decrypted_payload_correct():
    decrypted_payload_path = "/home/user/decrypted_payload.txt"
    assert os.path.isfile(decrypted_payload_path), f"File {decrypted_payload_path} is missing."

    with open(decrypted_payload_path, "r") as f:
        content = f.read().strip()

    expected_payload = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAmaliciouskey attacker@host"
    assert content == expected_payload, f"Expected decrypted payload to be '{expected_payload}', but got '{content}'."