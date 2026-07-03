# test_final_state.py

import os
import json
import stat
import tarfile
import subprocess
import pytest

LOG_FILE = "/home/user/provision.log"
BACKUPS_DIR = "/home/user/backups"
APP_DATA_DIR = "/home/user/app_data"

def test_provision_log_exists_and_valid():
    assert os.path.exists(LOG_FILE), f"{LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{LOG_FILE} is not a valid JSON file.")

    expected_keys = {"pid", "backup_file", "tz"}
    assert expected_keys.issubset(log_data.keys()), f"JSON must contain keys: {expected_keys}"

def test_provision_log_contents():
    with open(LOG_FILE, "r") as f:
        log_data = json.load(f)

    assert log_data.get("tz") == "Asia/Tokyo", "The 'tz' key must be 'Asia/Tokyo'."

    pid = log_data.get("pid")
    assert isinstance(pid, int), "The 'pid' key must be an integer."

    # Check if process is running
    try:
        output = subprocess.check_output(["ps", "-p", str(pid), "-o", "args="], text=True).strip()
        assert "python3" in output and "-m" in output and "http.server" in output and "9999" in output, \
            f"Process with PID {pid} is not running the expected command. Found: {output}"
    except subprocess.CalledProcessError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_backup_directory_permissions():
    assert os.path.isdir(BACKUPS_DIR), f"Directory {BACKUPS_DIR} does not exist."
    dir_stat = os.stat(BACKUPS_DIR)
    mode = stat.S_IMODE(dir_stat.st_mode)
    assert mode == 0o700, f"Directory {BACKUPS_DIR} must have 0700 permissions, got {oct(mode)}."

def test_backup_file_validity():
    with open(LOG_FILE, "r") as f:
        log_data = json.load(f)

    backup_path = log_data.get("backup_file")
    assert isinstance(backup_path, str), "The 'backup_file' key must be a string."
    assert backup_path.startswith(f"{BACKUPS_DIR}/app_backup_"), "Backup file must start with /home/user/backups/app_backup_"
    assert backup_path.endswith(".tar.gz"), "Backup file must end with .tar.gz"

    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    file_stat = os.stat(backup_path)
    mode = stat.S_IMODE(file_stat.st_mode)
    assert mode == 0o600, f"Backup file must have 0600 permissions, got {oct(mode)}."

    assert tarfile.is_tarfile(backup_path), f"Backup file {backup_path} is not a valid tarball."

    # Check tarball contents
    with tarfile.open(backup_path, "r:gz") as tar:
        names = tar.getnames()
        # Ensure config.yml and data.txt are in the tarball
        has_config = any(name.endswith("config.yml") for name in names)
        has_data = any(name.endswith("data.txt") for name in names)
        assert has_config, "config.yml not found in the backup tarball."
        assert has_data, "data.txt not found in the backup tarball."