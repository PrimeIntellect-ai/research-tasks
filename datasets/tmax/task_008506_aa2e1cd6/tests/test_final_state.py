# test_final_state.py

import os
import json
import pytest

def test_malicious_files_txt():
    filepath = "/home/user/malicious_files.txt"
    assert os.path.exists(filepath), f"File {filepath} does not exist."
    assert os.path.isfile(filepath), f"{filepath} is not a file."

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_malicious_paths = {
        "../../../home/user/ssh_keys.txt",
        "/var/run/daemon.pid",
        "safe_dir/../../etc/passwd"
    }

    actual_paths = set(lines)

    missing = expected_malicious_paths - actual_paths
    extra = actual_paths - expected_malicious_paths

    assert not missing, f"Missing malicious paths in {filepath}: {missing}"
    assert not extra, f"Extra/incorrect paths found in {filepath}: {extra}"

def test_safe_backup_directory():
    dirpath = "/home/user/safe_backup"
    assert os.path.exists(dirpath), f"Directory {dirpath} does not exist."
    assert os.path.isdir(dirpath), f"{dirpath} is not a directory."

    extracted_files = set(os.listdir(dirpath))
    expected_files = {"config.ini", "01.wal", "02.wal"}

    missing = expected_files - extracted_files
    extra = extracted_files - expected_files

    assert not missing, f"Missing safe files in {dirpath}: {missing}"
    assert not extra, f"Malicious or extra files extracted to {dirpath}: {extra}"

def test_final_config_json():
    filepath = "/home/user/final_config.json"
    assert os.path.exists(filepath), f"File {filepath} does not exist."
    assert os.path.isfile(filepath), f"{filepath} is not a file."

    with open(filepath, 'r') as f:
        try:
            actual_config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} does not contain valid JSON.")

    expected_config = {
        "backup_dir": "/data/backup/daily/v2",
        "max_retries": "5",
        "alert_port": "8080",
        "new_feature": "enabled"
    }

    assert isinstance(actual_config, dict), "The JSON object should be a dictionary."

    for key, expected_val in expected_config.items():
        assert key in actual_config, f"Key '{key}' is missing from final configuration."
        assert actual_config[key] == expected_val, f"Value for '{key}' is incorrect. Expected '{expected_val}', got '{actual_config[key]}'."

    for key in actual_config:
        assert key in expected_config, f"Unexpected key '{key}' found in final configuration."