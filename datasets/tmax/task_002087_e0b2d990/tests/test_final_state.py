# test_final_state.py

import os
import pytest

def test_archive_exists_and_size_metric():
    archive_path = "/home/user/final_backup.fsa"
    assert os.path.isfile(archive_path), f"Archive file missing: {archive_path}"

    file_size = os.path.getsize(archive_path)
    threshold = 4500000
    assert file_size <= threshold, f"Archive size is {file_size} bytes, which exceeds the threshold of {threshold} bytes. The archiver may not have been compiled with the correct optimization flags."

def test_files_converted_to_utf8():
    for i in range(1, 51):
        file_path = f"/home/user/legacy_data/project_a/file_{i}.txt"
        assert os.path.isfile(file_path), f"File missing: {file_path}"

        with open(file_path, "rb") as f:
            content = f.read()

        try:
            content.decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail(f"File {file_path} is not valid UTF-8. The encoding conversion step failed or was not performed.")

def test_daemon_script_exists():
    script_path = "/home/user/backup_daemon.sh"
    assert os.path.isfile(script_path), f"Backup daemon script missing: {script_path}"

def test_fast_archiver_binary_exists():
    binary_path = "/home/user/bin/fast-archiver"
    assert os.path.isfile(binary_path), f"Compiled fast-archiver binary missing at expected path: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"fast-archiver binary at {binary_path} is not executable"