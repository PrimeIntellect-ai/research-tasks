# test_final_state.py

import os
import tarfile
import pytest

def test_backup_exists_and_valid():
    """Check if the backup tarball exists and contains the expected files."""
    backup_file = "/home/user/backup/manifests.tar.gz"
    assert os.path.isfile(backup_file), f"Backup file {backup_file} does not exist."

    try:
        with tarfile.open(backup_file, "r:gz") as tar:
            names = [os.path.basename(m.name) for m in tar.getmembers() if m.isfile()]
            assert "deploy.yaml" in names, "deploy.yaml is missing from the backup tarball."
            assert "service.yaml" in names, "service.yaml is missing from the backup tarball."
    except tarfile.ReadError:
        pytest.fail(f"Backup file {backup_file} is not a valid gzip-compressed tarball.")

def test_processed_deploy_yaml():
    """Check if processed deploy.yaml exists and contains the correct JST timestamp."""
    path = "/home/user/processed/deploy.yaml"
    assert os.path.isfile(path), f"Processed file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    expected_annotation = 'deployed-at: "2023-11-01 17:30:00 JST"'
    assert expected_annotation in content, f"File {path} does not contain the expected converted timestamp: {expected_annotation}"

def test_processed_service_yaml():
    """Check if processed service.yaml exists and contains the correct JST timestamp."""
    path = "/home/user/processed/service.yaml"
    assert os.path.isfile(path), f"Processed file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    expected_annotation = 'deployed-at: "2023-11-01 18:15:00 JST"'
    assert expected_annotation in content, f"File {path} does not contain the expected converted timestamp: {expected_annotation}"

def test_timestamps_txt_content():
    """Check if timestamps.txt exists and contains the correctly sorted extracted values."""
    path = "/home/user/timestamps.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        '"2023-11-01 17:30:00 JST"',
        '"2023-11-01 18:15:00 JST"'
    ]

    assert lines == expected_lines, f"Content of {path} does not match the expected sorted timestamps. Got: {lines}"