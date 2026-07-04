# test_final_state.py

import os
import hashlib
import pytest

def test_restore_script_exists_and_executable():
    script_path = "/home/user/restore.sh"
    assert os.path.isfile(script_path), f"Restore script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Restore script {script_path} is not executable."

def test_restored_logs_contents():
    restored_dir = "/home/user/restored_logs"
    assert os.path.isdir(restored_dir), f"Directory {restored_dir} does not exist."

    expected_files = {"app_20220315.log", "app_20220620.log", "app_20221105.log"}
    actual_files = set(os.listdir(restored_dir))

    assert actual_files == expected_files, f"Restored logs directory contains {actual_files}, expected {expected_files}."

def test_archived_chunks_sizes():
    chunks_dir = "/home/user/archived_chunks"
    assert os.path.isdir(chunks_dir), f"Directory {chunks_dir} does not exist."

    chunks = sorted([f for f in os.listdir(chunks_dir) if f.startswith("archive.part.")])
    assert len(chunks) > 0, "No archive chunks found starting with 'archive.part.'."

    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(chunks_dir, chunk)
        size = os.path.getsize(chunk_path)
        if i < len(chunks) - 1:
            assert size == 2097152, f"Chunk {chunk} has size {size}, expected exactly 2097152 bytes."
        else:
            assert size <= 2097152, f"Last chunk {chunk} has size {size}, expected <= 2097152 bytes."

def test_restored_checksums():
    checksum_file = "/home/user/restored_checksums.txt"
    assert os.path.isfile(checksum_file), f"Checksum file {checksum_file} does not exist."

    original_logs_dir = "/home/user/logs"
    expected_files = sorted(["app_20220315.log", "app_20220620.log", "app_20221105.log"])

    expected_lines = []
    for filename in expected_files:
        filepath = os.path.join(original_logs_dir, filename)
        assert os.path.isfile(filepath), f"Original log file {filepath} missing."

        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        expected_lines.append(f"{sha256_hash.hexdigest()}  {filename}")

    with open(checksum_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "Checksum file contents do not match the expected SHA256 hashes and filenames."