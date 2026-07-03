# test_final_state.py

import os
import tarfile
import pytest

def test_archiver_executable_exists():
    executable_path = "/home/user/archiver"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_archiver_c_source_code():
    source_path = "/home/user/archiver.c"
    assert os.path.isfile(source_path), f"Source code {source_path} does not exist."

    with open(source_path, 'r') as f:
        content = f.read()

    assert "sys/inotify.h" in content, f"{source_path} does not include sys/inotify.h"
    assert "IN_CLOSE_WRITE" in content, f"{source_path} does not use IN_CLOSE_WRITE"

def test_hot_data_is_empty():
    hot_data_dir = "/home/user/hot_data"
    assert os.path.isdir(hot_data_dir), f"Directory {hot_data_dir} does not exist."

    files = os.listdir(hot_data_dir)
    assert len(files) == 0, f"Directory {hot_data_dir} is not empty. Contains: {files}"

def test_cold_archive_contains_valid_archives():
    cold_archive_dir = "/home/user/cold_archive"
    assert os.path.isdir(cold_archive_dir), f"Directory {cold_archive_dir} does not exist."

    expected_files = ["report.csv", "image.bin", "system.log"]

    for filename in expected_files:
        archive_name = f"{filename}.tar.gz"
        archive_path = os.path.join(cold_archive_dir, archive_name)

        assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

        # Check if it's a valid tar.gz and contains the file
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                names = tar.getnames()
                assert filename in names or f"./{filename}" in names or f"/{filename}" in names, \
                    f"Archive {archive_name} does not contain {filename}."
        except tarfile.TarError:
            pytest.fail(f"Archive {archive_path} is not a valid gzip-compressed tar archive.")

def test_audit_log_contents():
    log_path = "/home/user/audit.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    expected_lines = [
        "ARCHIVED AND VERIFIED: report.csv",
        "ARCHIVED AND VERIFIED: image.bin",
        "ARCHIVED AND VERIFIED: system.log"
    ]

    for line in expected_lines:
        assert line in content, f"Audit log does not contain expected line: '{line}'"