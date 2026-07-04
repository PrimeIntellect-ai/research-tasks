# test_final_state.py

import os
import hashlib
import pytest

def test_deprecated_records_content():
    output_file = "/home/user/docs/deprecated_records.txt"
    assert os.path.isfile(output_file), f"Output file does not exist: {output_file}"

    # The expected content based on the setup script
    expected_content = (
        "Date: 2020-02-15\n"
        "Update: V1 API DEPRECATED.\n"
        "Please use V2.\n"
        "===RECORD===\n"
        "Date: 2021-08-20\n"
        "Update: The old authentication method is now DEPRECATED\n"
        "and will be removed in V3.\n"
        "===RECORD===\n"
    )

    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            actual_content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"File {output_file} is not valid UTF-8.")

    assert actual_content == expected_content, f"Content of {output_file} does not match the expected output."

def test_manifest_checksum():
    output_file = "/home/user/docs/deprecated_records.txt"
    manifest_file = "/home/user/docs/manifest.txt"

    assert os.path.isfile(manifest_file), f"Manifest file does not exist: {manifest_file}"
    assert os.path.isfile(output_file), f"Output file does not exist: {output_file}"

    # Compute actual SHA-256 of the output file
    sha256_hash = hashlib.sha256()
    with open(output_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    actual_checksum = sha256_hash.hexdigest()

    # Read the manifest file
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest_content = f.read().strip()

    # The manifest should contain the checksum and the filename, e.g., "<hash>  /home/user/docs/deprecated_records.txt"
    # We just check if the actual checksum is present in the manifest file
    assert actual_checksum in manifest_content, (
        f"Manifest file {manifest_file} does not contain the correct SHA-256 checksum.\n"
        f"Expected checksum: {actual_checksum}\n"
        f"Manifest content: {manifest_content}"
    )