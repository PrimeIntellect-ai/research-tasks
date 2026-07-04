# test_final_state.py

import os
import hashlib
import pytest

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_files_moved_correctly():
    expected_moved_files = [
        "/home/user/organized_protos/telecom/ecc/v1/hamming_encoder.proto",
        "/home/user/organized_protos/storage/verification/file_verifier.proto"
    ]

    for filepath in expected_moved_files:
        assert os.path.isfile(filepath), f"Expected file {filepath} was not found. It may not have been moved correctly or the directory structure is wrong."

def test_files_not_moved():
    expected_left_files = [
        "/home/user/grpc_project/math_basic.proto",
        "/home/user/grpc_project/random_stuff.proto"
    ]

    for filepath in expected_left_files:
        assert os.path.isfile(filepath), f"File {filepath} should not have been moved."

def test_manifest_correctness():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    expected_files = [
        "/home/user/organized_protos/storage/verification/file_verifier.proto",
        "/home/user/organized_protos/telecom/ecc/v1/hamming_encoder.proto"
    ]

    expected_lines = []
    for filepath in expected_files:
        if os.path.isfile(filepath):
            checksum = get_sha256(filepath)
            expected_lines.append(f"{checksum}  {filepath}")

    expected_lines.sort()

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Manifest has {len(actual_lines)} lines, expected {len(expected_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Manifest line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"