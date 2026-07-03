# test_final_state.py

import os
import pytest

def test_backup_file_size():
    backup_path = "/home/user/backup.gz"

    assert os.path.exists(backup_path), f"Expected backup file {backup_path} does not exist."
    assert os.path.isfile(backup_path), f"Expected {backup_path} to be a regular file."

    file_size = os.path.getsize(backup_path)

    threshold = 1000
    assert file_size < threshold, (
        f"Backup file size is {file_size} bytes, which is >= {threshold} bytes. "
        "This indicates the symlink loop was not properly fixed or "
        "the backup contains duplicate/incorrect data."
    )

    assert file_size > 0, "Backup file is empty (0 bytes), which means no data was processed."