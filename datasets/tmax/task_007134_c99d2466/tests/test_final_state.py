# test_final_state.py

import os
import struct
import pytest

def test_processed_log():
    path = "/home/user/processed_log.bin"
    assert os.path.isfile(path), f"Missing file: {path}"

    expected_records = [
        (1690000000, 0x0A000001, b"\x00" * 21),
        (1690000005, 0x0A000002, b"A" * 55),
        (1690000010, 0x0A000003, b"\xde\xad\xbe\xef" + b"B" * 124),
        (1690000015, 0x0A000004, b"\x00" * 15)
    ]

    expected_content = b""
    for ts, ip, token in expected_records:
        expected_content += struct.pack("<I I H", ts, ip, len(token))
        expected_content += token

    with open(path, "rb") as f:
        content = f.read()

    assert content == expected_content, f"Content of {path} does not match expected processed state."

def test_crash_token():
    path = "/home/user/crash_token.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    expected_token = b"\xde\xad\xbe\xef" + b"B" * 124
    expected_hex = expected_token.hex().upper()

    with open(path, "r") as f:
        content = f.read()

    assert content == expected_hex, f"Content of {path} does not match expected crash token hex string."

def test_exploit_bin():
    path = "/home/user/exploit.bin"
    assert os.path.isfile(path), f"Missing file: {path}"

    expected_token = b"\xde\xad\xbe\xef" + b"A" * 124
    expected_content = struct.pack("<I I H", 1700000000, 0x01020304, 128) + expected_token

    with open(path, "rb") as f:
        content = f.read()

    assert content == expected_content, f"Content of {path} does not match the expected exploit payload."