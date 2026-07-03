# test_final_state.py

import os
import json
import tarfile
import pytest

def test_current_backup_exists_and_files_copied():
    current_backup = '/home/user/current_backup'
    assert os.path.isdir(current_backup), f"{current_backup} is not a directory or does not exist."

    expected_files = ['app.ini', 'db.ini', 'cache.ini']
    for f in expected_files:
        path = os.path.join(current_backup, f)
        assert os.path.isfile(path), f"File {path} is missing from the backup."

def test_hard_links_correctly_applied():
    last_backup_db = '/home/user/last_backup/db.ini'
    current_backup_db = '/home/user/current_backup/db.ini'

    assert os.path.exists(last_backup_db) and os.path.exists(current_backup_db), "db.ini files missing"

    last_db_stat = os.stat(last_backup_db)
    curr_db_stat = os.stat(current_backup_db)

    assert last_db_stat.st_ino == curr_db_stat.st_ino, (
        "db.ini in current_backup is not a hard link to last_backup/db.ini "
        "(inodes do not match)."
    )

    last_backup_app = '/home/user/last_backup/app.ini'
    current_backup_app = '/home/user/current_backup/app.ini'

    assert os.path.exists(last_backup_app) and os.path.exists(current_backup_app), "app.ini files missing"

    last_app_stat = os.stat(last_backup_app)
    curr_app_stat = os.stat(current_backup_app)

    assert last_app_stat.st_ino != curr_app_stat.st_ino, (
        "app.ini in current_backup should NOT be a hard link to last_backup/app.ini "
        "(inodes should not match because contents differ)."
    )

def test_summary_json_content():
    summary_path = '/home/user/current_backup/summary.json'
    assert os.path.isfile(summary_path), f"{summary_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{summary_path} is not a valid JSON file.")

    expected_data = {
        "EXPORT_APP_PORT": "8081",
        "EXPORT_APP_MODE": "production",
        "EXPORT_DB_HOST": "localhost",
        "EXPORT_DB_PORT": "5432",
        "EXPORT_CACHE_TTL": "3600"
    }

    assert data == expected_data, f"Parsed JSON data does not match expected output. Got: {data}"

def test_symlink_latest_backup():
    symlink_path = '/home/user/latest_backup'
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    # The target could be absolute or relative, but it must resolve to /home/user/current_backup
    resolved_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    assert resolved_target == '/home/user/current_backup', (
        f"{symlink_path} does not point to /home/user/current_backup. Points to {resolved_target}."
    )

def test_tar_archive_contents():
    archive_path = '/home/user/backup.tar.gz'
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, 'r:gz') as tar:
        members = tar.getnames()

        # Check that the required files exist inside the current_backup/ directory in the tar
        expected_members = [
            'current_backup/app.ini',
            'current_backup/db.ini',
            'current_backup/cache.ini',
            'current_backup/summary.json'
        ]

        for expected in expected_members:
            # allow for ./current_backup/... or current_backup/...
            found = any(m.endswith(expected) for m in members)
            assert found, f"Expected file {expected} not found in the tar archive."