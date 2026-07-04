# test_final_state.py

import os
import pytest

def test_backup_directory_and_contents():
    backup_dir = "/home/user/backup"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist."

    for i in range(1, 51):
        num_str = f"{i:02d}"
        backup_file = os.path.join(backup_dir, f"doc_{num_str}.md")

        assert os.path.isfile(backup_file), f"Backup file {backup_file} is missing."

        with open(backup_file, "r") as f:
            content = f.read()

        assert f"ID: {num_str}" in content, f"Original ID missing in backup {backup_file}."
        assert "State: WORK_IN_PROGRESS" in content, f"State was modified in backup {backup_file}!"
        assert f"Location: /home/user/docs/doc_{num_str}.md" in content, f"Location was modified in backup {backup_file}!"

def test_docs_directory_renamed_and_edited():
    docs_dir = "/home/user/docs"

    for i in range(1, 51):
        num_str = f"{i:02d}"
        old_file = os.path.join(docs_dir, f"doc_{num_str}.md")
        new_file = os.path.join(docs_dir, f"rel_{num_str}.md")

        assert not os.path.exists(old_file), f"Old file {old_file} still exists. It should have been renamed."
        assert os.path.isfile(new_file), f"New file {new_file} is missing."

        with open(new_file, "r") as f:
            content = f.read()

        assert f"ID: {num_str}" in content, f"ID missing in {new_file}."
        assert "State: RELEASED" in content, f"State not correctly updated to RELEASED in {new_file}."
        assert f"Location: {new_file}" in content, f"Location not correctly updated in {new_file}."

def test_inodes_are_split():
    backup_dir = "/home/user/backup"
    docs_dir = "/home/user/docs"

    for i in range(1, 51):
        num_str = f"{i:02d}"
        backup_file = os.path.join(backup_dir, f"doc_{num_str}.md")
        new_file = os.path.join(docs_dir, f"rel_{num_str}.md")

        if os.path.isfile(backup_file) and os.path.isfile(new_file):
            stat_backup = os.stat(backup_file)
            stat_new = os.stat(new_file)
            assert stat_backup.st_ino != stat_new.st_ino, (
                f"Inodes match for {backup_file} and {new_file}! "
                "The program edited the hard link in-place, ruining the snapshot."
            )