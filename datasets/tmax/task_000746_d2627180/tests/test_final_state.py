# test_final_state.py

import os
import pytest

def test_backup_tar_exists():
    path = "/home/user/backup.tar"
    assert os.path.isfile(path), f"Expected backup archive at {path} is missing. Did the script successfully interact with fetch_backup?"

def test_metadata_extracted():
    path = "/home/user/mnt_restore/metadata.json"
    assert os.path.isfile(path), f"Expected extracted file at {path} is missing. Did the script extract the tarball?"

def test_fstab_updated():
    path = "/home/user/mock_root/etc/fstab"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    expected_line = "/home/user/backup.tar /home/user/mnt_restore tarfs ro,nosuid,nodev 0 0"
    assert expected_line in content, "The fstab file does not contain the expected backup mount entry."
    assert "/dev/sda1" in content, "The original contents of the fstab file were not preserved."

def test_restore_status_log():
    path = "/home/user/restore_status.log"
    assert os.path.isfile(path), f"Log file {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "USER_VERIFIED: backup_admin", f"Expected log content 'USER_VERIFIED: backup_admin', but got '{content}'."

def test_script_exists():
    path = "/home/user/restore_automation.py"
    assert os.path.isfile(path), f"The automation script {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    # Basic static analysis to ensure proxy ports are mentioned
    assert "9999" in content, "The script does not seem to contain the proxy listening port 9999."
    assert "8080" in content, "The script does not seem to contain the proxy destination port 8080."