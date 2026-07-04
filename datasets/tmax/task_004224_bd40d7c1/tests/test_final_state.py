# test_final_state.py

import os
import tarfile
import pytest

def test_c_files_exist():
    assert os.path.isfile("/home/user/provision_backup.c"), "C source file /home/user/provision_backup.c is missing."
    assert os.path.isfile("/home/user/provision_backup"), "Executable /home/user/provision_backup is missing."
    assert os.access("/home/user/provision_backup", os.X_OK), "Executable /home/user/provision_backup is not executable."

def test_provision_log_contents():
    log_file = "/home/user/provision.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert "BACKUP_SUCCESS: alice" in lines, "Missing BACKUP_SUCCESS: alice in log."
    assert "QUOTA_EXCEEDED: bob" in lines, "Missing QUOTA_EXCEEDED: bob in log."
    assert "BACKUP_SUCCESS: charlie" in lines, "Missing BACKUP_SUCCESS: charlie in log."

def test_backup_files():
    alice_backup = "/home/user/backups/alice_backup.tar.gz"
    charlie_backup = "/home/user/backups/charlie_backup.tar.gz"
    bob_backup = "/home/user/backups/bob_backup.tar.gz"

    assert os.path.isfile(alice_backup), f"Backup file {alice_backup} should exist."
    assert os.path.isfile(charlie_backup), f"Backup file {charlie_backup} should exist."
    assert not os.path.exists(bob_backup), f"Backup file {bob_backup} should NOT exist because bob exceeded quota."

def test_tarball_contents():
    alice_backup = "/home/user/backups/alice_backup.tar.gz"
    charlie_backup = "/home/user/backups/charlie_backup.tar.gz"

    if os.path.isfile(alice_backup):
        with tarfile.open(alice_backup, "r:gz") as tar:
            names = tar.getnames()
            assert any(name.endswith("file.txt") for name in names), "Alice's backup does not contain file.txt."

    if os.path.isfile(charlie_backup):
        with tarfile.open(charlie_backup, "r:gz") as tar:
            names = tar.getnames()
            assert any(name.endswith("file.txt") for name in names), "Charlie's backup does not contain file.txt."