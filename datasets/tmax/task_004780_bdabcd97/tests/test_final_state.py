# test_final_state.py

import os
import json
import hashlib
import pytest

ARTIFACTS_DIR = "/home/user/artifacts"
RAW_DATA_FILE = os.path.join(ARTIFACTS_DIR, "raw_data.bin")
METADATA_FILE = os.path.join(ARTIFACTS_DIR, "metadata.txt")
COMPRESSED_FILE = os.path.join(ARTIFACTS_DIR, "compressed.bin")
MANIFEST_FILE = os.path.join(ARTIFACTS_DIR, "final_manifest.json")

def rle_encode(data: bytes) -> bytes:
    """Helper to compute the expected RLE sequence."""
    if not data:
        return b""

    encoded = bytearray()
    current_byte = data[0]
    count = 1

    for byte in data[1:]:
        if byte == current_byte and count < 255:
            count += 1
        else:
            encoded.append(count)
            encoded.append(current_byte)
            current_byte = byte
            count = 1

    encoded.append(count)
    encoded.append(current_byte)

    return bytes(encoded)

def test_compressed_bin_exists_and_correct():
    """Test that compressed.bin exists and contains the correctly encoded RLE data."""
    assert os.path.isfile(COMPRESSED_FILE), f"File {COMPRESSED_FILE} does not exist."
    assert os.path.isfile(RAW_DATA_FILE), f"Source file {RAW_DATA_FILE} is missing."

    with open(RAW_DATA_FILE, 'rb') as f:
        raw_data = f.read()

    expected_compressed_data = rle_encode(raw_data)

    with open(COMPRESSED_FILE, 'rb') as f:
        actual_compressed_data = f.read()

    assert actual_compressed_data == expected_compressed_data, \
        f"Content of {COMPRESSED_FILE} does not match the expected RLE encoded data."

def test_final_manifest_exists_and_correct():
    """Test that final_manifest.json exists, is valid JSON, and contains the correct metadata and checksum."""
    assert os.path.isfile(MANIFEST_FILE), f"File {MANIFEST_FILE} does not exist."
    assert os.path.isfile(METADATA_FILE), f"Source file {METADATA_FILE} is missing."
    assert os.path.isfile(COMPRESSED_FILE), f"Source file {COMPRESSED_FILE} is missing."

    # Compute expected metadata
    with open(METADATA_FILE, 'rb') as f:
        raw_metadata = f.read()
    expected_metadata_text = raw_metadata.decode('utf-16le')

    # Compute expected checksum
    with open(COMPRESSED_FILE, 'rb') as f:
        compressed_data = f.read()
    expected_checksum = hashlib.sha256(compressed_data).hexdigest()

    # Read and parse actual manifest
    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        try:
            manifest_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {MANIFEST_FILE} as JSON: {e}")

    assert "metadata" in manifest_data, "Manifest is missing the 'metadata' key."
    assert "checksum" in manifest_data, "Manifest is missing the 'checksum' key."

    assert manifest_data["metadata"] == expected_metadata_text, \
        f"Manifest metadata does not match the decoded content of {METADATA_FILE}."

    assert manifest_data["checksum"] == expected_checksum, \
        f"Manifest checksum does not match the SHA-256 hash of {COMPRESSED_FILE}."