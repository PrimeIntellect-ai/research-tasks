# test_final_state.py

import os
import re
import pytest

def test_backup_archive_exists():
    assert os.path.isdir("/home/user/backup_archive"), "Directory /home/user/backup_archive was not created."

def test_backed_up_files():
    active_config_path = "/home/user/backup_archive/active_config.json"
    settings_path = "/home/user/backup_archive/settings.json"

    assert os.path.isfile(active_config_path), "active_config.json was not backed up."
    assert os.path.isfile(settings_path), "settings.json was not backed up."

def test_not_backed_up_files():
    assert not os.path.isfile("/home/user/backup_archive/old_config.json"), "old_config.json should not be backed up (mtime is older than last backup)."
    assert not os.path.isfile("/home/user/backup_archive/legacy.json"), "legacy.json should not be backed up (mtime is older than last backup)."
    assert not os.path.isfile("/home/user/backup_archive/data.xml"), "data.xml should not be backed up (wrong extension)."

def test_backup_report_yaml():
    yaml_path = "/home/user/backup_report.yaml"
    assert os.path.isfile(yaml_path), "backup_report.yaml was not created."

    with open(yaml_path, 'r') as f:
        content = f.read()

    assert "backed_up_files:" in content, "The key 'backed_up_files:' is missing in the YAML report."

    # Extract filenames and sizes using regex since third-party yaml libraries are not allowed
    filenames = re.findall(r'filename:\s*["\']?(.*?)["\']?(?:\n|$)', content)
    sizes = re.findall(r'size:\s*(\d+)', content)

    assert len(filenames) == 2, f"Expected 2 filenames in the report, found {len(filenames)}."
    assert len(sizes) == 2, f"Expected 2 sizes in the report, found {len(sizes)}."

    # Check if sorted alphabetically
    assert filenames == sorted(filenames), "Filenames in the report are not sorted alphabetically."

    # Check exact filenames
    assert filenames[0] == "active_config.json", f"Expected active_config.json as the first file, got {filenames[0]}"
    assert filenames[1] == "settings.json", f"Expected settings.json as the second file, got {filenames[1]}"

    # Dynamically check sizes based on the original files
    active_size = os.path.getsize("/home/user/app_configs/sub2/active_config.json")
    settings_size = os.path.getsize("/home/user/app_configs/settings.json")

    assert int(sizes[0]) == active_size, f"Incorrect size for active_config.json: expected {active_size}, got {sizes[0]}"
    assert int(sizes[1]) == settings_size, f"Incorrect size for settings.json: expected {settings_size}, got {sizes[1]}"