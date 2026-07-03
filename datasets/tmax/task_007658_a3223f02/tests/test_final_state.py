# test_final_state.py

import os
import glob
import tarfile
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/config_tracker.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_directories_exist():
    dirs = [
        "/home/user/legacy_configs",
        "/home/user/staging",
        "/home/user/backups"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_backup_files():
    backups_dir = "/home/user/backups"
    tar_files = glob.glob(os.path.join(backups_dir, "backup_*.tar.gz"))
    assert len(tar_files) == 2, f"Expected exactly 2 tar.gz files in {backups_dir}, found {len(tar_files)}."

    snar_file = os.path.join(backups_dir, "snapshot.snar")
    assert os.path.isfile(snar_file), f"Snapshot file {snar_file} does not exist."

def test_latest_tarball_contents():
    backups_dir = "/home/user/backups"
    tar_files = glob.glob(os.path.join(backups_dir, "backup_*.tar.gz"))
    assert tar_files, "No backup tar.gz files found."

    # Sort by modification time to get the latest
    latest_tar = max(tar_files, key=os.path.getmtime)

    with tarfile.open(latest_tar, "r:gz") as tar:
        names = tar.getnames()

        # Check that app.conf is in the archive
        has_app_conf = any(name.endswith("app.conf") for name in names)
        assert has_app_conf, f"app.conf not found in the latest tarball {latest_tar}."

        # Check that db.conf is NOT in the archive
        has_db_conf = any(name.endswith("db.conf") for name in names)
        assert not has_db_conf, f"db.conf should not be in the latest incremental tarball {latest_tar}."

        # Extract app.conf to verify its content and encoding
        app_conf_member = next(m for m in tar.getmembers() if m.name.endswith("app.conf"))
        f = tar.extractfile(app_conf_member)
        content = f.read()

        try:
            text_content = content.decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail("app.conf in the latest tarball is not valid UTF-8.")

        assert "téléphone=12345" in text_content, "Expected text 'téléphone=12345' not found in app.conf."
        assert "serveur=dédié" in text_content, "Expected text 'serveur=dédié' not found in app.conf."

def test_latest_archived_log():
    log_file = "/home/user/latest_archived.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r", encoding="utf-8", errors="replace") as f:
        log_content = f.read()

    assert "app.conf" in log_content, "app.conf is missing from latest_archived.log."
    assert "db.conf" not in log_content, "db.conf should not be in latest_archived.log."