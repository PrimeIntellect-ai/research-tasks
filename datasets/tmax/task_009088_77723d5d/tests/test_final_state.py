# test_final_state.py

import os
import struct
import hashlib
import pytest

def test_clean_manifest_exists_and_correct():
    path = "/home/user/clean_manifest.txt"
    assert os.path.isfile(path), f"Clean manifest {path} does not exist."

    with open(path, "r") as f:
        lines = f.read().splitlines()

    expected_lines = ["blob1.bin", "configs/sys.conf", "data_payload.bin"]
    assert lines == expected_lines, f"Clean manifest contents are incorrect. Expected {expected_lines}, got {lines}"

def test_repo_archive_bin_structure_and_contents():
    archive_path = "/home/user/repo_archive.bin"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    unpacked_dir = "/home/user/unpacked"
    manifest_files = ["blob1.bin", "configs/sys.conf", "data_payload.bin"]

    with open(archive_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"ARTF", f"Invalid magic bytes in archive. Expected b'ARTF', got {magic}"

        for expected_path in manifest_files:
            # Read path length
            path_len_bytes = f.read(2)
            assert len(path_len_bytes) == 2, "Unexpected EOF reading path length."
            path_len = struct.unpack("=H", path_len_bytes)[0]
            assert path_len == len(expected_path), f"Path length mismatch. Expected {len(expected_path)}, got {path_len}"

            # Read path string
            path_str_bytes = f.read(path_len)
            assert len(path_str_bytes) == path_len, "Unexpected EOF reading path string."
            path_str = path_str_bytes.decode('utf-8', errors='replace')
            assert path_str == expected_path, f"Path string mismatch. Expected {expected_path}, got {path_str}"

            # Read chunk count
            chunk_count_bytes = f.read(4)
            assert len(chunk_count_bytes) == 4, "Unexpected EOF reading chunk count."
            chunk_count = struct.unpack("=I", chunk_count_bytes)[0]

            # Verify against actual file
            actual_file_path = os.path.join(unpacked_dir, expected_path)
            assert os.path.isfile(actual_file_path), f"Expected unpacked file {actual_file_path} is missing."

            with open(actual_file_path, "rb") as af:
                actual_data = af.read()

            expected_chunk_count = (len(actual_data) + 1023) // 1024
            if len(actual_data) == 0:
                expected_chunk_count = 0

            assert chunk_count == expected_chunk_count, f"Chunk count mismatch for {expected_path}. Expected {expected_chunk_count}, got {chunk_count}"

            reconstructed_data = b""
            for i in range(chunk_count):
                chunk_size_bytes = f.read(2)
                assert len(chunk_size_bytes) == 2, f"Unexpected EOF reading chunk size for chunk {i} of {expected_path}."
                chunk_size = struct.unpack("=H", chunk_size_bytes)[0]

                chunk_data = f.read(chunk_size)
                assert len(chunk_data) == chunk_size, f"Unexpected EOF reading chunk data for chunk {i} of {expected_path}."

                reconstructed_data += chunk_data

            assert reconstructed_data == actual_data, f"Data mismatch for {expected_path}. Extracted data does not match original."

        extra_data = f.read(1)
        assert extra_data == b"", "Archive contains trailing data after the expected files."

def test_archive_hash_correct():
    hash_path = "/home/user/archive_hash.txt"
    archive_path = "/home/user/repo_archive.bin"

    assert os.path.isfile(hash_path), f"Hash file {hash_path} does not exist."
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    with open(hash_path, "r") as f:
        written_hash = f.read().strip()

    with open(archive_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    assert written_hash == actual_hash, f"Hash mismatch. File contains {written_hash}, but actual SHA-256 is {actual_hash}."