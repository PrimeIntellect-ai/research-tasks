# test_final_state.py
import os
import pytest

def test_corrupted_log():
    """Test that the corrupted log contains the correct filenames."""
    log_path = '/home/user/corrupted.log'
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_corrupted = ['backup_03.tar.gz', 'backup_05.zip']
    assert lines == expected_corrupted, f"Expected {expected_corrupted} in corrupted.log, but got {lines}"

def test_all_configs_yaml():
    """Test that the all_configs.yaml file contains the correct content."""
    yaml_path = '/home/user/all_configs.yaml'
    assert os.path.exists(yaml_path), f"{yaml_path} does not exist."

    with open(yaml_path, 'r') as f:
        content = f.read().strip()

    # Check for expected source headers
    assert "# Source: backup_01.zip" in content, "Missing source header for backup_01.zip"
    assert "# Source: backup_02.tar.gz" in content, "Missing source header for backup_02.tar.gz"
    assert "# Source: backup_04.zip" in content, "Missing source header for backup_04.zip"

    # Check for specific yaml content lines
    assert "theme: dark" in content, "Missing expected yaml content: theme: dark"
    assert "theme: light" in content, "Missing expected yaml content: theme: light"
    assert "- auth" in content, "Missing expected yaml content: - auth"
    assert "theme: blue" in content, "Missing expected yaml content: theme: blue"
    assert "version: 1" in content, "Missing expected yaml content: version: 1"
    assert "version: 2" in content, "Missing expected yaml content: version: 2"
    assert "version: 4" in content, "Missing expected yaml content: version: 4"

    # Ensure no corrupted files are in the yaml
    assert "backup_03.tar.gz" not in content, "Corrupted file backup_03.tar.gz should not be in all_configs.yaml"
    assert "backup_05.zip" not in content, "Corrupted file backup_05.zip should not be in all_configs.yaml"