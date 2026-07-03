# test_final_state.py

import os
import subprocess
import pytest

def test_backup_archive_exists_and_size():
    archive_path = '/home/user/backup.bin'
    assert os.path.exists(archive_path), f"Backup archive not found at {archive_path}"
    assert os.path.isfile(archive_path), f"{archive_path} is not a file"

    size = os.path.getsize(archive_path)
    threshold = 45000
    assert size <= threshold, f"Archive size {size} bytes exceeds the {threshold} bytes threshold. You need to improve compression."

def test_backup_archive_extractable():
    archive_path = '/home/user/backup.bin'
    extract_dir = '/tmp/extract_test'

    # Ensure the extract directory exists or can be created by the unpacker
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir, exist_ok=True)

    result = subprocess.run(
        ['/app/config_unpacker', archive_path, extract_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"config_unpacker failed to extract the archive.\n"
        f"STDOUT: {result.stdout}\n"
        f"STDERR: {result.stderr}"
    )