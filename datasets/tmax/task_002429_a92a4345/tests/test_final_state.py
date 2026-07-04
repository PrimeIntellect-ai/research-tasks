# test_final_state.py

import os
import json
import pytest

def test_backup_directory_contents():
    """Verify that the backup directory contains the original files before transformation."""
    backup_base = "/home/user/backup_drive/projects_backup"

    expected_files = {
        os.path.join(backup_base, "proj_alpha", "users.csv"): "id,username,role\n1,admin,superuser\n2,bob,editor",
        os.path.join(backup_base, "proj_beta", "settings.json"): '{"theme": "dark"}',
        os.path.join(backup_base, "proj_beta", "sub_dir", "metrics.csv"): "date,clicks,views\n2023-01-01,50,1000\n2023-01-02,75,1200"
    }

    for filepath, expected_content in expected_files.items():
        assert os.path.isfile(filepath), f"Backup file missing: {filepath}"
        with open(filepath, "r") as f:
            content = f.read().strip()
            assert content == expected_content.strip(), f"Content mismatch in backup file {filepath}"

def test_no_csv_files_in_old_projects():
    """Verify that no .csv files remain in the old_projects directory."""
    old_projects_base = "/home/user/old_projects"

    csv_files = []
    for root, dirs, files in os.walk(old_projects_base):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    assert len(csv_files) == 0, f"Found remaining .csv files in {old_projects_base}: {csv_files}"

def test_json_conversion_contents():
    """Verify that the .csv files were correctly converted to .json."""
    users_json_path = "/home/user/old_projects/proj_alpha/users.json"
    metrics_json_path = "/home/user/old_projects/proj_beta/sub_dir/metrics.json"

    assert os.path.isfile(users_json_path), f"Converted JSON file missing: {users_json_path}"
    assert os.path.isfile(metrics_json_path), f"Converted JSON file missing: {metrics_json_path}"

    with open(users_json_path, "r") as f:
        users_data = json.load(f)

    expected_users_data = [
        {"id": "1", "username": "admin", "role": "superuser"},
        {"id": "2", "username": "bob", "role": "editor"}
    ]
    assert users_data == expected_users_data, f"JSON content mismatch in {users_json_path}"

    with open(metrics_json_path, "r") as f:
        metrics_data = json.load(f)

    expected_metrics_data = [
        {"date": "2023-01-01", "clicks": "50", "views": "1000"},
        {"date": "2023-01-02", "clicks": "75", "views": "1200"}
    ]
    assert metrics_data == expected_metrics_data, f"JSON content mismatch in {metrics_json_path}"

def test_existing_json_untouched():
    """Verify that the existing JSON file was not modified."""
    settings_json_path = "/home/user/old_projects/proj_beta/settings.json"
    assert os.path.isfile(settings_json_path), f"Existing JSON file missing: {settings_json_path}"

    with open(settings_json_path, "r") as f:
        settings_data = json.load(f)

    assert settings_data == {"theme": "dark"}, f"Existing JSON file was modified: {settings_json_path}"

def test_conversion_log():
    """Verify the contents of the conversion log."""
    log_path = "/home/user/conversion_log.txt"
    assert os.path.isfile(log_path), f"Conversion log missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "/home/user/old_projects/proj_alpha/users.json",
        "/home/user/old_projects/proj_beta/sub_dir/metrics.json"
    ]

    assert lines == expected_lines, f"Log contents mismatch or not sorted correctly. Expected {expected_lines}, got {lines}"