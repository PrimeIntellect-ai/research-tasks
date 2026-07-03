# test_final_state.py

import os
import tarfile
import pytest

def test_backup_out_exists_and_contains_added_files():
    out_path = "/home/user/backup.out"
    assert os.path.isfile(out_path), f"Standard output file {out_path} does not exist."

    with open(out_path, "r") as f:
        content = f.read()

    assert "Added access.log" in content, "backup.out is missing 'Added access.log'"
    assert "Added app.log" in content, "backup.out is missing 'Added app.log'"
    assert "Added dump.sql" in content, "backup.out is missing 'Added dump.sql'"

def test_archive_exists_and_is_valid_tar_gz():
    archive_path = "/home/user/backups/sanitized_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

def test_archive_contents_and_sanitization():
    archive_path = "/home/user/backups/sanitized_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()

        # Check files are at root level
        for member in members:
            assert "/" not in member, f"File {member} is not at the root level of the archive."

        assert "access.log" in members, "access.log is missing from the archive."
        assert "app.log" in members, "app.log is missing from the archive."
        assert "dump.sql" in members, "dump.sql is missing from the archive."

        # Check access.log
        access_log_f = tar.extractfile("access.log")
        assert access_log_f is not None, "Could not extract access.log"
        access_log_content = access_log_f.read().decode("utf-8")
        assert "XXX.XXX.XXX.XXX GET /index.html 200" in access_log_content, "access.log not properly sanitized"
        assert "XXX.XXX.XXX.XXX POST /api/data 500" in access_log_content, "access.log not properly sanitized"
        assert "XXX.XXX.XXX.XXX GET /health 200" in access_log_content, "access.log not properly sanitized"
        assert "192.168.1.100" not in access_log_content, "Original IP found in access.log"
        assert "10.0.0.5" not in access_log_content, "Original IP found in access.log"

        # Check app.log
        app_log_f = tar.extractfile("app.log")
        assert app_log_f is not None, "Could not extract app.log"
        app_log_content = app_log_f.read().decode("utf-8")
        assert "[INFO] Server started at XXX.XXX.XXX.XXX" in app_log_content, "app.log not properly sanitized"
        assert "[ERROR] Database connection failed from XXX.XXX.XXX.XXX" in app_log_content, "app.log not properly sanitized"
        assert "172.16.0.2" not in app_log_content, "Original IP found in app.log"
        assert "127.0.0.1" not in app_log_content, "Original IP found in app.log"

        # Check dump.sql (should be unmodified)
        dump_sql_f = tar.extractfile("dump.sql")
        assert dump_sql_f is not None, "Could not extract dump.sql"
        dump_sql_content = dump_sql_f.read().decode("utf-8")
        assert "INSERT INTO users (id, name) VALUES (1, 'admin');" in dump_sql_content, "dump.sql was modified"
        assert "INSERT INTO logs (ip) VALUES ('192.168.1.1');" in dump_sql_content, "dump.sql was modified (IPs should not be sanitized in .sql files)"

def test_original_files_unmodified():
    # access.log
    log_path = "/home/user/data_source/access.log"
    assert os.path.isfile(log_path), f"Original file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read()
    assert "192.168.1.100 GET /index.html 200" in content, "Original access.log was modified."
    assert "10.0.0.5 POST /api/data 500" in content, "Original access.log was modified."

    # app.log
    app_log_path = "/home/user/data_source/app.log"
    assert os.path.isfile(app_log_path), f"Original file {app_log_path} is missing."
    with open(app_log_path, "r") as f:
        content = f.read()
    assert "[INFO] Server started at 172.16.0.2" in content, "Original app.log was modified."
    assert "[ERROR] Database connection failed from 127.0.0.1" in content, "Original app.log was modified."