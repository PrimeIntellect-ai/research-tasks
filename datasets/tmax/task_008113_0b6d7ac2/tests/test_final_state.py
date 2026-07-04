# test_final_state.py

import os
import hashlib
import pytest

RAW_DIR = "/home/user/artifacts/raw"
LATEST_DIR = "/home/user/artifacts/latest"

def decode_rle(blob_path):
    """Decodes the custom RLE format from the given blob file."""
    with open(blob_path, 'rb') as f:
        data = f.read()

    out = bytearray()
    for i in range(0, len(data), 2):
        if i + 1 >= len(data):
            break
        count = data[i]
        if count == 0:
            break
        value = data[i+1]
        out.extend(bytes([value]) * count)
    return bytes(out)

def get_blob_files(directory):
    blob_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".blob"):
                blob_files.append(os.path.join(root, file))
    return blob_files

def test_latest_directory_exists():
    """Test that the latest directory was created."""
    assert os.path.exists(LATEST_DIR), f"Directory {LATEST_DIR} does not exist."
    assert os.path.isdir(LATEST_DIR), f"{LATEST_DIR} is not a directory."

def test_decompressed_files_and_symlinks():
    """Test that all .blob files are decompressed correctly and symlinked."""
    blob_files = get_blob_files(RAW_DIR)
    assert len(blob_files) > 0, f"No .blob files found in {RAW_DIR}."

    expected_symlinks = set()

    for blob_path in blob_files:
        # Decode the expected content
        expected_content = decode_rle(blob_path)

        # Check the .bin file
        bin_path = blob_path[:-5] + ".bin"
        assert os.path.exists(bin_path), f"Decompressed file missing: {bin_path}"
        assert os.path.isfile(bin_path), f"Expected file, found directory: {bin_path}"

        with open(bin_path, 'rb') as f:
            actual_content = f.read()

        assert actual_content == expected_content, f"Content mismatch in {bin_path}. Expected {expected_content}, got {actual_content}"

        # Calculate SHA256
        sha256_hash = hashlib.sha256(expected_content).hexdigest()
        symlink_name = f"{sha256_hash}.bin"
        symlink_path = os.path.join(LATEST_DIR, symlink_name)

        expected_symlinks.add(symlink_name)

        # Check the symlink
        assert os.path.exists(symlink_path), f"Symlink missing: {symlink_path}"
        assert os.path.islink(symlink_path), f"Expected symlink, but it is not a link: {symlink_path}"

        target_path = os.readlink(symlink_path)
        assert target_path == bin_path, f"Symlink {symlink_path} points to {target_path}, expected absolute path {bin_path}"

def test_no_extra_symlinks_in_latest():
    """Test that the latest directory contains exactly the expected symlinks and nothing else."""
    blob_files = get_blob_files(RAW_DIR)
    expected_symlinks = set()
    for blob_path in blob_files:
        expected_content = decode_rle(blob_path)
        sha256_hash = hashlib.sha256(expected_content).hexdigest()
        expected_symlinks.add(f"{sha256_hash}.bin")

    if os.path.exists(LATEST_DIR):
        actual_files = set(os.listdir(LATEST_DIR))
        extra_files = actual_files - expected_symlinks
        missing_files = expected_symlinks - actual_files

        assert not extra_files, f"Found unexpected files in {LATEST_DIR}: {extra_files}"
        assert not missing_files, f"Missing expected files in {LATEST_DIR}: {missing_files}"