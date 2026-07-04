# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_system_check_untouched():
    path = "/home/user/system_check.txt"
    assert os.path.exists(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert content == "SAFE\n", f"File {path} was modified! Expected 'SAFE\\n', got {content!r}"

def test_clean_logs_tar_exists():
    path = "/home/user/clean_logs.tar.gz"
    assert os.path.exists(path), f"File {path} is missing."
    assert tarfile.is_tarfile(path), f"File {path} is not a valid tar archive."

def test_clean_logs_contents():
    path = "/home/user/clean_logs.tar.gz"
    assert os.path.exists(path), f"File {path} is missing."

    with tarfile.open(path, "r:gz") as tar:
        members = tar.getmembers()

        # Ensure flattened structure (no directories in paths)
        names = [m.name for m in members if m.isfile()]
        assert sorted(names) == ["app.log", "db.log"], f"Expected 'app.log' and 'db.log' at the root of the archive, got {names}"

        # Check app.log content
        app_log_member = tar.getmember("app.log")
        app_log_content = tar.extractfile(app_log_member).read().decode('utf-8')
        assert "API_KEY: REDACTED" in app_log_content, "app.log does not contain 'API_KEY: REDACTED'"
        assert "aB39xZ" not in app_log_content, "app.log still contains the original API_KEY"

        # Check db.log content
        db_log_member = tar.getmember("db.log")
        db_log_content = tar.extractfile(db_log_member).read().decode('utf-8')
        assert "API_KEY: REDACTED" in db_log_content, "db.log does not contain 'API_KEY: REDACTED'"
        assert "99xYz1" not in db_log_content, "db.log still contains the original API_KEY"