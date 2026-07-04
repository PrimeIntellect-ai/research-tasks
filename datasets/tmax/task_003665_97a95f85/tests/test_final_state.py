# test_final_state.py

import os
import tarfile
import pytest

def test_removed_links_file():
    filepath = "/home/user/removed_links.txt"
    assert os.path.isfile(filepath), f"Expected output file {filepath} does not exist."

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/backup_source/archive/old/loop_to_root",
        "/home/user/backup_source/projects/alpha/loop_to_projects"
    ]

    assert lines == expected_lines, f"Contents of {filepath} do not match the expected sorted list of removed links. Got: {lines}"

def test_symlinks_deleted():
    loop1 = "/home/user/backup_source/projects/alpha/loop_to_projects"
    loop2 = "/home/user/backup_source/archive/old/loop_to_root"

    assert not os.path.exists(loop1) and not os.path.islink(loop1), f"Symlink {loop1} was not deleted."
    assert not os.path.exists(loop2) and not os.path.islink(loop2), f"Symlink {loop2} was not deleted."

def test_valid_symlink_remains():
    valid_link = "/home/user/backup_source/projects/alpha/readme_link.md"
    assert os.path.islink(valid_link), f"Valid symlink {valid_link} was incorrectly deleted or modified."

def test_archive_created_and_valid():
    archive_path = "/home/user/successful_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Backup archive {archive_path} was not created."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
    except tarfile.TarError:
        pytest.fail(f"File {archive_path} is not a valid tar.gz archive.")

    # Check that the base directory is included
    assert any(name == "backup_source" or name.startswith("backup_source/") for name in names), \
        "Archive must contain the base directory 'backup_source'."

    # Ensure deleted symlinks are not in the archive
    # Tar names might be relative (e.g., 'backup_source/projects/alpha/loop_to_projects')
    # or absolute (e.g., '/home/user/backup_source/projects/alpha/loop_to_projects')
    # We will check if the specific paths end with the bad symlink names
    for name in names:
        assert not name.endswith("loop_to_projects"), f"Archive incorrectly contains deleted link: {name}"
        assert not name.endswith("loop_to_root"), f"Archive incorrectly contains deleted link: {name}"

    # Ensure valid symlink is in the archive
    assert any(name.endswith("readme_link.md") for name in names), "Archive is missing the valid symlink 'readme_link.md'."