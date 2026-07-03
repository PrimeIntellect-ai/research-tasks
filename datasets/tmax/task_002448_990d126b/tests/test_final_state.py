# test_final_state.py

import os
import tarfile
import pytest

def test_symlink_exists_and_correct():
    symlink_path = '/home/user/latest_archive'
    assert os.path.islink(symlink_path), f"Symlink {symlink_path} does not exist or is not a symlink."

    target = os.readlink(symlink_path)
    expected_targets = ['/home/user/logs/archive.tar.gz', 'logs/archive.tar.gz']
    assert target in expected_targets, f"Symlink points to {target}, expected one of {expected_targets}."

def test_archive_size():
    archive_path = '/home/user/logs/archive.tar.gz'
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    size = os.path.getsize(archive_path)
    threshold = 180
    assert size <= threshold, f"Archive size is {size} bytes, which exceeds the threshold of {threshold} bytes. Did you use maximum compression?"

def test_archive_contents():
    archive_path = '/home/user/logs/archive.tar.gz'
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    expected_files = ['sanitized_service1.log', 'sanitized_service2.log', 'sanitized_service3.log']

    with tarfile.open(archive_path, 'r:gz') as tar:
        # Get basenames of files in the archive
        archive_members = [os.path.basename(m.name) for m in tar.getmembers() if m.isfile()]

        for expected in expected_files:
            assert expected in archive_members, f"Expected file {expected} not found in the archive."

        # Check contents
        for member in tar.getmembers():
            if not member.isfile() or not member.name.endswith('.log'):
                continue

            f = tar.extractfile(member)
            content = f.read().decode('utf-8')

            assert "SECRET_KEY" not in content, f"Found unreplaced 'SECRET_KEY' in {member.name} inside the archive."
            assert "REDACTED_KEY" in content, f"Expected 'REDACTED_KEY' not found in {member.name} inside the archive."