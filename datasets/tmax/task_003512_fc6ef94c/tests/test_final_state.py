# test_final_state.py

import os
import hashlib
import pytest

def test_extracted_files_content():
    extracted_dir = "/home/user/extracted"
    assert os.path.exists(extracted_dir), f"Directory {extracted_dir} does not exist."
    assert os.path.isdir(extracted_dir), f"Path {extracted_dir} is not a directory."

    expected_files = {
        "alpha.bin": bytes([0x0A, 0x0B, 0xFF, 0xFF, 0xFF, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x0D, 0xFF, 0xFF, 0xFF]),
        "beta.bin": bytes([0xFF, 0xAA, 0xFF, 0xFF, 0xFF, 0xBB, 0x00, 0x00, 0xCC]),
        "gamma.bin": bytes([0x11, 0x22, 0x33, 0x44, 0x55])
    }

    for fname, expected_bytes in expected_files.items():
        file_path = os.path.join(extracted_dir, fname)
        assert os.path.exists(file_path), f"Extracted file {file_path} is missing."
        assert os.path.isfile(file_path), f"Path {file_path} is not a file."

        with open(file_path, "rb") as f:
            actual_bytes = f.read()

        assert actual_bytes == expected_bytes, f"Content of {file_path} is incorrect. Expected {expected_bytes.hex()}, got {actual_bytes.hex()}."

def test_manifest_file_content():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} is missing."
    assert os.path.isfile(manifest_path), f"Path {manifest_path} is not a file."

    expected_manifest_lines = [
        "8f36cfae2e8e3d085938d8d4ec08dfeb0de8f51a4461bb3bc5e933e4b752496a  alpha.bin",
        "a15a818c99f935f8d6d84ce5a59f5188828b6d37012678f5f64d084c8a16fa9c  beta.bin",
        "08b534608c02452c6f1cd0b8c667a4d5218d6e3c0429df92a3d76e3381e4b868  gamma.bin"
    ]

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_manifest_lines, f"Manifest content is incorrect. Expected:\n{chr(10).join(expected_manifest_lines)}\nGot:\n{chr(10).join(actual_lines)}"