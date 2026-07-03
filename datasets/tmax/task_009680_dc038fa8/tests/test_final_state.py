# test_final_state.py

import os
import json
import gzip
import hashlib
import pytest

ARCHIVE_DIR = "/home/user/dataset/archive"
RAW_FILE = "/home/user/dataset/raw_sensor.log"
CHUNK_SIZE = 1048576

def test_chunk_files_exist():
    """Test that exactly the expected chunk files exist."""
    expected_chunks = ["chunk_0000.gz", "chunk_0001.gz", "chunk_0002.gz"]
    for chunk in expected_chunks:
        chunk_path = os.path.join(ARCHIVE_DIR, chunk)
        assert os.path.isfile(chunk_path), f"Expected chunk file {chunk} is missing in {ARCHIVE_DIR}"

def test_no_tmp_files():
    """Test that no temporary files remain in the archive directory."""
    files = os.listdir(ARCHIVE_DIR)
    tmp_files = [f for f in files if f.startswith(".tmp")]
    assert len(tmp_files) == 0, f"Found temporary files in {ARCHIVE_DIR}: {tmp_files}"

def test_reconstructed_data():
    """Test that uncompressing and concatenating the chunks matches the original file."""
    expected_chunks = ["chunk_0000.gz", "chunk_0001.gz", "chunk_0002.gz"]
    reconstructed = b""

    for chunk in expected_chunks:
        chunk_path = os.path.join(ARCHIVE_DIR, chunk)
        assert os.path.isfile(chunk_path), f"Missing {chunk_path}"
        with gzip.open(chunk_path, "rb") as f:
            reconstructed += f.read()

    assert os.path.isfile(RAW_FILE), f"Original file {RAW_FILE} is missing"
    with open(RAW_FILE, "rb") as f:
        original_data = f.read()

    assert reconstructed == original_data, "Reconstructed data from chunks does not match the original raw_sensor.log"

def test_manifest_json():
    """Test that manifest.json exists, is valid, and contains the correct hashes."""
    manifest_path = os.path.join(ARCHIVE_DIR, "manifest.json")
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing"

    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not valid JSON")

    assert isinstance(manifest, list), "Manifest should be a JSON array"

    expected_chunks = ["chunk_0000.gz", "chunk_0001.gz", "chunk_0002.gz"]
    assert len(manifest) == len(expected_chunks), f"Manifest should contain {len(expected_chunks)} entries"

    # Calculate actual hashes of the original file chunks
    actual_hashes = []
    with open(RAW_FILE, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            actual_hashes.append(hashlib.sha256(data).hexdigest())

    assert len(actual_hashes) == len(expected_chunks), "Unexpected number of chunks in original file"

    manifest_dict = {}
    for entry in manifest:
        assert isinstance(entry, dict), "Manifest entry should be a JSON object"
        assert "chunk" in entry, "Manifest entry missing 'chunk' key"
        assert "original_sha256" in entry, "Manifest entry missing 'original_sha256' key"
        manifest_dict[entry["chunk"]] = entry["original_sha256"]

    for i, chunk_name in enumerate(expected_chunks):
        assert chunk_name in manifest_dict, f"{chunk_name} missing from manifest"
        assert manifest_dict[chunk_name] == actual_hashes[i], f"Hash mismatch for {chunk_name}: expected {actual_hashes[i]}, got {manifest_dict[chunk_name]}"