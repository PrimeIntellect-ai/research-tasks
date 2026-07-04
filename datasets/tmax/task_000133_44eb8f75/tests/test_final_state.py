# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_logs_are_symlinks():
    logs_dir = "/home/user/data/logs"
    placeholder = "/home/user/data/offline_placeholder.txt"
    expected_logs = ["app_alpha.log", "app_beta.log", "app_gamma.log"]

    for log_name in expected_logs:
        log_path = os.path.join(logs_dir, log_name)
        assert os.path.islink(log_path), f"Log file {log_path} is not a symlink."
        target = os.readlink(log_path)
        assert target == placeholder, f"Symlink {log_path} points to {target}, expected {placeholder}."

def test_archive_chunks_exist_and_sized_correctly():
    archive_dir = "/home/user/data/archive"
    chunk_files = sorted([f for f in os.listdir(archive_dir) if f.startswith("chunk_") and f.endswith(".dat")])

    assert len(chunk_files) > 0, "No chunk files found in the archive directory."

    # Check naming convention
    for i, f in enumerate(chunk_files):
        expected_name = f"chunk_{i:03d}.dat"
        assert f == expected_name, f"Expected chunk name {expected_name}, found {f}."

    # Check sizes (all but last must be exactly 1MB)
    chunk_size = 1048576
    for f in chunk_files[:-1]:
        file_path = os.path.join(archive_dir, f)
        size = os.path.getsize(file_path)
        assert size == chunk_size, f"Chunk {f} has size {size}, expected {chunk_size}."

    # Last chunk should be <= 1MB and > 0
    last_chunk_path = os.path.join(archive_dir, chunk_files[-1])
    last_size = os.path.getsize(last_chunk_path)
    assert 0 < last_size <= chunk_size, f"Last chunk {chunk_files[-1]} has invalid size {last_size}."

def test_reconstruct_and_verify_tarball():
    archive_dir = "/home/user/data/archive"
    chunk_files = sorted([f for f in os.listdir(archive_dir) if f.startswith("chunk_") and f.endswith(".dat")])

    assert len(chunk_files) > 0, "No chunk files found to reconstruct."

    with tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz") as temp_tar:
        temp_tar_path = temp_tar.name
        for f in chunk_files:
            chunk_path = os.path.join(archive_dir, f)
            with open(chunk_path, "rb") as chunk_file:
                temp_tar.write(chunk_file.read())

    try:
        assert tarfile.is_tarfile(temp_tar_path), "Reconstructed file is not a valid tar archive."

        with tarfile.open(temp_tar_path, "r:gz") as tar:
            members = tar.getnames()

            # The exact paths in the tarball might depend on how the student created it
            # (e.g. relative vs absolute paths, but it must contain the file names)
            member_basenames = [os.path.basename(m) for m in members]

            expected_logs = ["app_alpha.log", "app_beta.log", "app_gamma.log"]
            for log in expected_logs:
                assert log in member_basenames, f"Expected log file {log} not found in reconstructed tarball."
    finally:
        if os.path.exists(temp_tar_path):
            os.remove(temp_tar_path)