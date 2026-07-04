# test_final_state.py

import os
import tarfile
import pytest

def test_incremental_backup_script_exists():
    script_path = '/home/user/incremental_backup.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_incremental_archive_exists_and_valid():
    archive_path = '/home/user/incremental.tar.gz'
    assert os.path.isfile(archive_path), f"The incremental backup archive {archive_path} was not created."
    assert tarfile.is_tarfile(archive_path), f"The file {archive_path} is not a valid tar archive."

def test_incremental_archive_contents():
    archive_path = '/home/user/incremental.tar.gz'
    assert os.path.isfile(archive_path), "Archive missing."

    with tarfile.open(archive_path, 'r:gz') as tar:
        names = tar.getnames()

        # 2. Check that symlink is ignored
        assert 'data_dir/subdir/loop' not in names, "The symlink 'data_dir/subdir/loop' should be ignored and not included in the archive."

        # 3. Check that unmodified files are not included
        assert 'data_dir/file1.txt' not in names, "Unmodified file 'data_dir/file1.txt' should not be in the incremental backup."
        assert 'data_dir/subdir/file3.txt' not in names, "Unmodified file 'data_dir/subdir/file3.txt' should not be in the incremental backup."

        # 4. Check that modified and new files are included
        assert 'data_dir/file2.txt' in names, "Modified file 'data_dir/file2.txt' was not found in the incremental backup."
        assert 'data_dir/new_file.txt' in names, "New file 'data_dir/new_file.txt' was not found in the incremental backup."

def test_backup_log_contents():
    log_path = '/home/user/backup_log.txt'
    assert os.path.isfile(log_path), f"The log file {log_path} was not created."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        'data_dir/file2.txt',
        'data_dir/new_file.txt'
    ]

    assert lines == expected_lines, (
        f"The contents of {log_path} do not match the expected output. "
        f"Expected: {expected_lines}, but got: {lines}"
    )