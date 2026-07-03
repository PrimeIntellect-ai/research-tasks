# test_final_state.py

import os
import pytest

def test_archive_exists():
    archive_path = "/home/user/archive.dat"
    assert os.path.exists(archive_path), f"Input file {archive_path} is missing."
    assert os.path.isfile(archive_path), f"{archive_path} should be a file."

def test_chunks_directory_exists():
    chunks_dir = "/home/user/chunks"
    assert os.path.exists(chunks_dir), f"Directory {chunks_dir} is missing."
    assert os.path.isdir(chunks_dir), f"{chunks_dir} should be a directory."

def test_manifest_and_chunks():
    archive_path = "/home/user/archive.dat"
    chunks_dir = "/home/user/chunks"
    manifest_path = os.path.join(chunks_dir, "manifest.txt")

    assert os.path.exists(archive_path), f"Archive {archive_path} missing."
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} missing."

    with open(archive_path, 'rb') as f:
        data = f.read()

    expected_manifest = []
    for i in range(0, len(data), 4096):
        chunk = data[i:i+4096]
        xor_sum = 0
        for b in chunk:
            xor_sum ^= b
        idx = i // 4096
        expected_manifest.append(f"chunk_{idx:04d}.dat {len(chunk)} {xor_sum:02x}")

    with open(manifest_path, 'r') as f:
        actual_manifest = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_manifest == expected_manifest, (
        f"Manifest mismatch.\nExpected:\n{expected_manifest}\nGot:\n{actual_manifest}"
    )

    # Verify chunk contents
    for i in range(0, len(data), 4096):
        idx = i // 4096
        chunk = data[i:i+4096]
        chunk_path = os.path.join(chunks_dir, f"chunk_{idx:04d}.dat")
        assert os.path.exists(chunk_path), f"Chunk {chunk_path} missing"
        with open(chunk_path, 'rb') as f:
            c_data = f.read()
        assert c_data == chunk, f"Data mismatch in chunk_{idx:04d}.dat"