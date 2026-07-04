# test_final_state.py

import os
import tarfile

def test_symlink_removed():
    symlink_path = "/home/user/data/documents/reports/archive_link"
    assert not os.path.exists(symlink_path) and not os.path.islink(symlink_path), \
        f"The symlink {symlink_path} still exists. It should have been deleted."

def test_loop_symlink_txt_content():
    log_file = "/home/user/loop_symlink.txt"
    assert os.path.isfile(log_file), f"The log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read().strip()

    expected_path = "/home/user/data/documents/reports/archive_link"
    assert content == expected_path, \
        f"The file {log_file} contains '{content}', but expected '{expected_path}'."

def test_backup_archive_exists_and_valid():
    archive_path = "/home/user/system_backup.tar.gz"
    assert os.path.isfile(archive_path), f"The backup archive {archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), \
        f"The file {archive_path} is not a valid tar archive."

def test_backup_archive_contents():
    archive_path = "/home/user/system_backup.tar.gz"

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()

        # Check that the symlink is not in the archive
        for name in names:
            assert "archive_link" not in name, \
                f"The archive contains the symlink or a reference to it: {name}"

        # Check that some expected files are present
        # Since the user could tar the directory itself or its contents, we check for basenames or relative paths
        file_basenames = [os.path.basename(name) for name in names]
        expected_files = ["2023_Q1.txt", "2023_Q2.txt", "photo.jpg"]

        for expected in expected_files:
            assert expected in file_basenames, \
                f"Expected file {expected} is missing from the backup archive."