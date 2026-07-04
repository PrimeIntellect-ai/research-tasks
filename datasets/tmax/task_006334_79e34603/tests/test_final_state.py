# test_final_state.py

import os
import tarfile

def test_extractor_cpp_exists():
    assert os.path.isfile("/home/user/extractor.cpp"), "C++ source file /home/user/extractor.cpp is missing."

def test_extractor_executable_exists():
    assert os.path.isfile("/home/user/extractor"), "Executable /home/user/extractor is missing."
    assert os.access("/home/user/extractor", os.X_OK), "/home/user/extractor is not executable."

def test_disk_errors_directory():
    assert os.path.isdir("/home/user/disk_errors"), "Directory /home/user/disk_errors is missing."
    files = sorted(os.listdir("/home/user/disk_errors"))
    expected_files = ["error_1.log", "error_2.log", "error_3.log"]
    assert files == expected_files, f"Expected files {expected_files} in /home/user/disk_errors, but got {files}."

def test_error_1_content():
    expected_content = """[2023-10-01 10:10:22] ERROR: Disk Space Critical
Module: StorageController
Traceback (most recent call last):
  File "storage.py", line 42, in check_space
    raise DiskFullException()
SESSION_TOKEN=REDACTED
"""
    with open("/home/user/disk_errors/error_1.log", "r") as f:
        content = f.read()
    assert content.strip() == expected_content.strip(), "Content of error_1.log does not match expected redacted output."

def test_error_2_content():
    expected_content = """[2023-10-01 10:15:30] ERROR: Disk Space Critical
Module: LogWriter
Details: Failed to write to /var/log/app.log
SESSION_TOKEN=REDACTED
Please free up space immediately.
"""
    with open("/home/user/disk_errors/error_2.log", "r") as f:
        content = f.read()
    assert content.strip() == expected_content.strip(), "Content of error_2.log does not match expected redacted output."

def test_error_3_content():
    expected_content = """[2023-10-01 10:20:00] ERROR: Disk Space Critical
Module: DatabaseSync
SESSION_TOKEN=REDACTED
Sync failed due to ENOSPC.
"""
    with open("/home/user/disk_errors/error_3.log", "r") as f:
        content = f.read()
    assert content.strip() == expected_content.strip(), "Content of error_3.log does not match expected redacted output."

def test_backup_archive_exists_and_valid():
    archive_path = "/home/user/errors_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Backup archive {archive_path} is missing."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
            # The archive should contain the directory and the 3 files.
            # Names might be like 'home/user/disk_errors/error_1.log' or 'disk_errors/error_1.log'
            # We just check if the basenames of the files are present.
            basenames = [os.path.basename(name) for name in names]
            assert "error_1.log" in basenames, "error_1.log missing from tarball."
            assert "error_2.log" in basenames, "error_2.log missing from tarball."
            assert "error_3.log" in basenames, "error_3.log missing from tarball."
    except tarfile.ReadError:
        assert False, f"File {archive_path} is not a valid gzip-compressed tarball."