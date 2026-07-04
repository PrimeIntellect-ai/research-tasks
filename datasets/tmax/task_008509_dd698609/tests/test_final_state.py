# test_final_state.py

import os
import json
import tarfile
import pytest

def test_renamed_files():
    expected_files = [
        "/home/user/server_configs/region_us/db_config.json",
        "/home/user/server_configs/region_us/web_config.json",
        "/home/user/server_configs/region_eu/app1/settings.xml",
        "/home/user/server_configs/region_eu/app1/legacy_cfg.json",
        "/home/user/server_configs/users.csv",
    ]

    unexpected_files = [
        "/home/user/server_configs/region_us/db_config.JSON",
        "/home/user/server_configs/region_us/web_config.JSON",
        "/home/user/server_configs/region_eu/app1/settings.XML",
        "/home/user/server_configs/region_eu/app1/legacy_cfg.JSON",
        "/home/user/server_configs/users.CSV",
    ]

    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected renamed file is missing: {file_path}"

    for file_path in unexpected_files:
        assert not os.path.exists(file_path), f"Old file with uppercase extension still exists: {file_path}"

def test_json_contents():
    db_config_path = "/home/user/server_configs/region_us/db_config.json"
    with open(db_config_path, 'r') as f:
        db_config = json.load(f)
    assert db_config.get("status") == "archived", "db_config.json should have status 'archived'"

    web_config_path = "/home/user/server_configs/region_us/web_config.json"
    with open(web_config_path, 'r') as f:
        web_config = json.load(f)
    assert web_config.get("status") == "active", "web_config.json should have status 'active'"

    legacy_cfg_path = "/home/user/server_configs/region_eu/app1/legacy_cfg.json"
    with open(legacy_cfg_path, 'r') as f:
        legacy_cfg = json.load(f)
    assert legacy_cfg.get("status") == "archived", "legacy_cfg.json should have status 'archived'"

def test_manifest_creation():
    manifest_path = "/home/user/manifest.csv"
    assert os.path.isfile(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/server_configs/region_eu/app1/legacy_cfg.json",
        "/home/user/server_configs/region_us/db_config.json"
    ]

    assert lines == expected_lines, f"Manifest contents are incorrect. Expected {expected_lines}, got {lines}"

def test_incremental_backup():
    backup_path = "/home/user/incremental_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Incremental backup missing: {backup_path}"
    assert tarfile.is_tarfile(backup_path), f"File is not a valid tar archive: {backup_path}"

    # Check if we can open it as a gzip tar
    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            members = tar.getnames()
            assert len(members) > 0, "Tar archive is empty"
    except Exception as e:
        pytest.fail(f"Failed to read gzipped tar archive: {e}")