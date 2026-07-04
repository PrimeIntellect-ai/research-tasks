# test_final_state.py

import os
import tarfile
import re
import pytest

def test_backup_tool_exists_and_uses_locking():
    source_file = "/home/user/backup_tool.go"
    assert os.path.isfile(source_file), f"Go source file {source_file} is missing."

    with open(source_file, "r") as f:
        content = f.read()

    # Check for some form of file locking mentioning the lock file
    assert "backup.lock" in content, "The code does not reference backup.lock."

    # Look for common locking mechanisms in Go (syscall.Flock, flock, etc.)
    lock_pattern = re.compile(r'(Flock|flock|Lock|lock)')
    assert lock_pattern.search(content), "No file locking mechanism found in the Go source code."

def test_backup_archive_exists():
    archive_path = "/home/user/backup_archive.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} was not created."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

def test_backup_archive_contents_and_redaction():
    archive_path = "/home/user/backup_archive.tar.gz"

    # We will extract into memory to check contents
    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()

        # Check for infinite loops by counting members
        assert len(members) < 50, "Tarball contains too many files, indicating an infinite symlink loop."

        # Get all file paths in the tarball
        member_names = [m.name for m in members]

        # Ensure paths are relative (e.g., app1/settings.csv, not /home/user/.../app1/settings.csv)
        for name in member_names:
            assert not name.startswith("/home/user"), f"Path {name} in tarball is absolute, should be relative."
            assert not name.startswith("/"), f"Path {name} in tarball is absolute, should be relative."

        # Verify expected files exist
        expected_csv1 = "app1/settings.csv"
        expected_csv2 = "app2/users.csv"

        # Sometimes paths might be prefixed with './'
        csv1_member = next((m for m in members if m.name.endswith(expected_csv1)), None)
        csv2_member = next((m for m in members if m.name.endswith(expected_csv2)), None)

        assert csv1_member is not None, f"{expected_csv1} is missing from the archive."
        assert csv2_member is not None, f"{expected_csv2} is missing from the archive."

        # Verify redaction in app1/settings.csv
        f1 = tar.extractfile(csv1_member)
        content1 = f1.read().decode('utf-8')
        assert "SECRET_KEY=REDACTED" in content1, "Redaction failed in app1/settings.csv."
        assert "9876QWERTY" not in content1, "Original secret still present in app1/settings.csv."

        # Verify redaction in app2/users.csv
        f2 = tar.extractfile(csv2_member)
        content2 = f2.read().decode('utf-8')
        assert content2.count("SECRET_KEY=REDACTED") == 2, "Redaction failed or incomplete in app2/users.csv."
        assert "admin123XYZ" not in content2, "Original secret still present in app2/users.csv."
        assert "guest000" not in content2, "Original secret still present in app2/users.csv."

def test_symlink_loop_avoidance_in_tarball():
    archive_path = "/home/user/backup_archive.tar.gz"

    with tarfile.open(archive_path, "r:gz") as tar:
        member_names = [m.name for m in tar.getmembers()]

        # If loops were followed infinitely, we'd see deeply nested paths
        # e.g., app1/loop_to_app2/loop_to_app1/loop_to_app2...
        for name in member_names:
            loop_count = name.count("loop_to_app")
            assert loop_count <= 2, f"Found deeply nested symlink path: {name}. Loop avoidance failed."