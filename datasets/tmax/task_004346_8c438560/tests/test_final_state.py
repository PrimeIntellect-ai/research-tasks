# test_final_state.py

import os
import struct
import hashlib

def test_extracted_password():
    path = "/home/user/extracted_password.txt"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    expected_password = "B@ckd00r_99!"
    assert content == expected_password, f"Expected extracted password to be '{expected_password}', but got '{content}'."

def test_compromised_ips():
    ips_path = "/home/user/compromised_ips.txt"
    traffic_path = "/home/user/traffic.bin"

    assert os.path.exists(ips_path), f"File {ips_path} is missing."
    assert os.path.exists(traffic_path), f"File {traffic_path} is missing."

    expected_ips = []
    with open(traffic_path, "rb") as f:
        while True:
            record = f.read(21)
            if not record or len(record) < 21:
                break
            ip_bytes = record[0:4]
            pwd_bytes = record[4:20]
            success = record[20]

            pwd_str = pwd_bytes.split(b'\x00')[0].decode('ascii', errors='ignore')
            if pwd_str == "B@ckd00r_99!" and success == 1:
                ip_str = ".".join(str(b) for b in ip_bytes)
                expected_ips.append(ip_str)

    with open(ips_path, "r") as f:
        actual_ips = [line.strip() for line in f.readlines() if line.strip()]

    assert set(actual_ips) == set(expected_ips), f"Expected IPs {expected_ips}, but got {actual_ips}."

def test_rotated_hash():
    hash_path = "/home/user/rotated_hash.txt"
    new_pass_path = "/home/user/new_password.txt"

    assert os.path.exists(hash_path), f"File {hash_path} is missing."
    assert os.path.exists(new_pass_path), f"File {new_pass_path} is missing."

    with open(new_pass_path, "r") as f:
        new_password = f.read()

    expected_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

    with open(hash_path, "r") as f:
        actual_hash = f.read()

    assert actual_hash == expected_hash, f"Expected hash '{expected_hash}', but got '{actual_hash}'."