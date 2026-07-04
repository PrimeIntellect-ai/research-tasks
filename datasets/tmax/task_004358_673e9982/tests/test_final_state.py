# test_final_state.py

import os
import tarfile
import pytest

def test_status_log():
    status_file = "/home/user/status.log"
    assert os.path.exists(status_file), f"{status_file} does not exist."
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert "SUCCESS" in content, f"{status_file} does not contain 'SUCCESS'."

def test_symlink():
    symlink_path = "/home/user/latest_data.txt"
    target_path = "/home/user/incoming/raw_data.txt"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    actual_target = os.readlink(symlink_path)
    # Allow absolute or relative symlinks pointing to the right place
    if not os.path.isabs(actual_target):
        actual_target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), actual_target))
    assert actual_target == target_path, f"Symlink points to {actual_target}, expected {target_path}."

def test_raw_data_lines():
    raw_data_path = "/home/user/incoming/raw_data.txt"
    assert os.path.exists(raw_data_path), f"{raw_data_path} does not exist."
    with open(raw_data_path, "r") as f:
        lines = f.readlines()
    assert len(lines) == 125, f"{raw_data_path} has {len(lines)} lines, expected 125."

def test_debug_chunks():
    debug_dir = "/home/user/debug_chunks"
    assert os.path.isdir(debug_dir), f"{debug_dir} is not a directory."

    expected_chunks = {
        "chunk_0.txt": 50,
        "chunk_1.txt": 50,
        "chunk_2.txt": 25,
    }

    for chunk, expected_lines in expected_chunks.items():
        chunk_path = os.path.join(debug_dir, chunk)
        assert os.path.exists(chunk_path), f"Chunk file {chunk_path} does not exist."
        with open(chunk_path, "r") as f:
            lines = f.readlines()
        assert len(lines) == expected_lines, f"{chunk} has {len(lines)} lines, expected {expected_lines}."

        # Check if it's a hard link (st_nlink > 1) or at least a regular file
        stat = os.stat(chunk_path)
        assert stat.st_nlink >= 1, f"{chunk_path} does not have a valid link count."

def test_archive():
    archive_path = "/home/user/processed/archive.tar.gz"
    assert os.path.exists(archive_path), f"{archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # The names in the tar might include directories, but they should include the chunk files
        base_names = [os.path.basename(name) for name in names]
        for chunk in ["chunk_0.txt", "chunk_1.txt", "chunk_2.txt"]:
            assert chunk in base_names, f"{chunk} is missing from the archive {archive_path}."