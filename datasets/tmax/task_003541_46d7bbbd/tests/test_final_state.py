# test_final_state.py

import os
import hashlib
import pytest

def test_manifest_exists_and_line_count():
    manifest_path = "/home/user/dataset/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in manifest.txt, found {len(lines)}"

def test_hard_links_correct():
    files_to_check = ["dataset_A.dat", "dataset_B.dat"]

    for filename in files_to_check:
        incoming_path = os.path.join("/home/user/dataset/incoming", filename)
        archive_path = os.path.join("/home/user/dataset/archive", filename)

        assert os.path.isfile(incoming_path), f"Original file missing: {incoming_path}"
        assert os.path.isfile(archive_path), f"Archived file missing: {archive_path}"

        stat_incoming = os.stat(incoming_path)
        stat_archive = os.stat(archive_path)

        assert stat_incoming.st_ino == stat_archive.st_ino, (
            f"File {archive_path} is not a hard link to {incoming_path} "
            f"(inodes: {stat_archive.st_ino} vs {stat_incoming.st_ino})"
        )

def test_chunk_files_sizes():
    expected_chunks = {
        "dataset_A_part0.bin": 100000,
        "dataset_A_part1.bin": 100000,
        "dataset_A_part2.bin": 50000,
        "dataset_B_part0.bin": 80000,
    }

    chunks_dir = "/home/user/dataset/chunks"
    assert os.path.isdir(chunks_dir), f"Chunks directory missing at {chunks_dir}"

    for chunk_name, expected_size in expected_chunks.items():
        chunk_path = os.path.join(chunks_dir, chunk_name)
        assert os.path.isfile(chunk_path), f"Expected chunk file missing: {chunk_path}"

        actual_size = os.path.getsize(chunk_path)
        assert actual_size == expected_size, (
            f"Chunk {chunk_name} has incorrect size. "
            f"Expected {expected_size}, got {actual_size}"
        )

def test_manifest_checksums():
    manifest_path = "/home/user/dataset/manifest.txt"
    chunks_dir = "/home/user/dataset/chunks"

    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, "Manifest should have exactly 4 entries."

    manifest_data = {}
    for line in lines:
        parts = line.split()
        assert len(parts) >= 2, f"Invalid manifest line format: '{line}'"
        checksum = parts[0]
        # Handle standard sha256sum output which might have an asterisk or space before filename
        filename = parts[-1].lstrip("*")
        manifest_data[filename] = checksum

    expected_filenames = [
        "dataset_A_part0.bin",
        "dataset_A_part1.bin",
        "dataset_A_part2.bin",
        "dataset_B_part0.bin"
    ]

    for expected_file in expected_filenames:
        # Some manifests might include the path or just the filename
        # We find the matching key in the manifest
        matching_keys = [k for k in manifest_data.keys() if k.endswith(expected_file)]
        assert matching_keys, f"File {expected_file} not found in manifest.txt"

        manifest_filename = matching_keys[0]
        expected_checksum = manifest_data[manifest_filename]

        chunk_path = os.path.join(chunks_dir, expected_file)
        assert os.path.isfile(chunk_path), f"Chunk file {chunk_path} missing"

        sha256 = hashlib.sha256()
        with open(chunk_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256.update(byte_block)

        actual_checksum = sha256.hexdigest()
        assert actual_checksum == expected_checksum, (
            f"Checksum mismatch for {expected_file}. "
            f"Manifest says {expected_checksum}, actual is {actual_checksum}"
        )