# test_final_state.py

import os
import tarfile
import pytest
import json

def test_clean_configs_extracted():
    clean_configs_dir = "/home/user/clean_configs/"
    assert os.path.isdir(clean_configs_dir), f"Directory {clean_configs_dir} is missing"

    files = set(os.listdir(clean_configs_dir))
    expected_files = {"db_config.json", "cache_config.json"}

    assert files == expected_files, f"Expected exactly {expected_files} in {clean_configs_dir}, but found {files}"

    # Check contents of the configs to ensure they are the correct ones
    with open(os.path.join(clean_configs_dir, "db_config.json"), "r") as f:
        db_config = json.load(f)
        assert db_config.get("db") == "mysql", "db_config.json content is incorrect"

    with open(os.path.join(clean_configs_dir, "cache_config.json"), "r") as f:
        cache_config = json.load(f)
        assert cache_config.get("cache") == "redis", "cache_config.json content is incorrect"

def test_critical_errors_log():
    log_path = "/home/user/critical_errors.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "CRITICAL: Database connection lost in app1",
        "CRITICAL: Out of memory in sys"
    ]

    # The instructions require the file to be sorted alphabetically
    expected_sorted = sorted(expected_lines)

    assert lines == expected_sorted, f"Expected sorted lines in {log_path}:\n{expected_sorted}\nBut got:\n{lines}"

def test_consolidated_configs_archive():
    archive_path = "/home/user/consolidated_configs.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} is missing"

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getnames()
    except Exception as e:
        pytest.fail(f"Failed to open {archive_path} as a tar.gz file: {e}")

    # The files should be at the root of the tarball (no directories)
    expected_members = {"db_config.json", "cache_config.json"}

    assert set(members) == expected_members, f"Expected exactly {expected_members} at the root of {archive_path}, but found {set(members)}"