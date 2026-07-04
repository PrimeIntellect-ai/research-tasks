# test_final_state.py
import os
import json
import pytest

def test_manifest_exists_and_valid():
    """Test that the manifest JSON file exists and is valid."""
    manifest_path = "/home/user/backup_manifest.json"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."
    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {manifest_path} is not valid JSON.")
    assert isinstance(data, list), f"Manifest JSON in {manifest_path} should be a list of objects."

def test_manifest_content():
    """Test that the manifest contains the exact expected mappings."""
    manifest_path = "/home/user/backup_manifest.json"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."
    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {manifest_path} is not valid JSON.")

    expected = [
        {"file_path": "/home/user/backup_source/db1/data.csv", "latest_id": 1050},
        {"file_path": "/home/user/backup_source/db1/old_data.csv", "latest_id": 999},
        {"file_path": "/home/user/backup_source/db2/logs/001.wal", "latest_id": 800},
        {"file_path": "/home/user/backup_source/db2/logs/002.wal", "latest_id": 2048}
    ]

    # Sort both lists by file_path to allow order-independent comparison
    data_sorted = sorted(data, key=lambda x: x.get("file_path", ""))
    expected_sorted = sorted(expected, key=lambda x: x["file_path"])

    assert data_sorted == expected_sorted, "Manifest content does not match the expected mappings."

def test_archive_dest_exists():
    """Test that the archive destination directory exists."""
    dest_path = "/home/user/archive_dest"
    assert os.path.isdir(dest_path), f"Archive destination directory {dest_path} is missing."

def test_archive_dest_contents():
    """Test that the archive destination contains exactly the filtered files with correct contents."""
    dest_path = "/home/user/archive_dest"
    assert os.path.isdir(dest_path), f"Archive destination directory {dest_path} is missing."

    files = set(os.listdir(dest_path))
    expected_files = {"data.csv", "002.wal"}
    assert files == expected_files, f"Archive directory contains {files}, expected exactly {expected_files}."

    # Check contents of data.csv
    with open("/home/user/backup_source/db1/data.csv", "r") as f:
        expected_data_csv = f.read()
    with open(os.path.join(dest_path, "data.csv"), "r") as f:
        archived_data_csv = f.read()
    assert archived_data_csv == expected_data_csv, "Archived data.csv content does not match the source file."

    # Check contents of 002.wal
    with open("/home/user/backup_source/db2/logs/002.wal", "r") as f:
        expected_002_wal = f.read()
    with open(os.path.join(dest_path, "002.wal"), "r") as f:
        archived_002_wal = f.read()
    assert archived_002_wal == expected_002_wal, "Archived 002.wal content does not match the source file."

def test_c_program_locking():
    """Test that the C program source code contains locking mechanisms."""
    c_path = "/home/user/manifest_generator.c"
    assert os.path.isfile(c_path), f"C program file {c_path} is missing."

    with open(c_path, "r") as f:
        content = f.read()

    assert "fcntl" in content or "flock" in content, "C program must use 'fcntl' or 'flock' locking mechanisms."