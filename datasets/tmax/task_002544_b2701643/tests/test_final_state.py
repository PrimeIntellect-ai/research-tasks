# test_final_state.py

import os
import tarfile
import pytest

def test_backup_go_fixed():
    backup_file = "/home/user/backup.go"
    assert os.path.isfile(backup_file), f"File {backup_file} does not exist"
    with open(backup_file, "r") as f:
        content = f.read()
    assert "/home/user/backups/users.tar.gz" in content, (
        "The Go backup script does not contain the correct absolute path '/home/user/backups/users.tar.gz'."
    )

def test_backup_archive_exists_and_valid():
    archive_path = "/home/user/backups/users.tar.gz"
    assert os.path.isfile(archive_path), f"Backup archive {archive_path} was not created."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
            assert "alice.txt" in names or "./alice.txt" in names, "alice.txt missing from the backup archive."
            assert "bob.txt" in names or "./bob.txt" in names, "bob.txt missing from the backup archive."
    except tarfile.TarError:
        pytest.fail(f"The file {archive_path} is not a valid gzip-compressed tar archive.")

def test_restored_data():
    alice_file = "/home/user/restored_data/alice.txt"
    bob_file = "/home/user/restored_data/bob.txt"

    assert os.path.isfile(alice_file), f"Restored file {alice_file} does not exist. Did the restore script run correctly?"
    with open(alice_file, "r") as f:
        assert f.read().strip() == "alice config", f"Content of {alice_file} is incorrect."

    assert os.path.isfile(bob_file), f"Restored file {bob_file} does not exist."
    with open(bob_file, "r") as f:
        assert f.read().strip() == "bob config", f"Content of {bob_file} is incorrect."

def test_expect_script():
    expect_script = "/home/user/test_restore.exp"
    assert os.path.isfile(expect_script), f"Expect script {expect_script} does not exist."

    with open(expect_script, "r") as f:
        content = f.read()

    assert "spawn" in content, f"'spawn' command missing from {expect_script}."
    assert "expect" in content, f"'expect' command missing from {expect_script}."
    assert "send" in content, f"'send' command missing from {expect_script}."
    assert "/home/user/backups/users.tar.gz" in content, f"The absolute backup path is missing from {expect_script}."

def test_fstab_entry():
    fstab_file = "/home/user/fstab_entry.txt"
    assert os.path.isfile(fstab_file), f"File {fstab_file} does not exist."

    with open(fstab_file, "r") as f:
        content = f.read().strip()

    expected_entry = "UUID=1234-5678-ABCD /home/user/backups ext4 defaults 0 2"
    assert content == expected_entry, (
        f"Contents of {fstab_file} are incorrect.\n"
        f"Expected: {expected_entry}\n"
        f"Found: {content}"
    )