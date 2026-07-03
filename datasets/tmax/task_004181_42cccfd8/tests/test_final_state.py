# test_final_state.py
import os
import pytest

def test_curator_script_exists_and_executable():
    curator_path = "/home/user/curator"
    assert os.path.isfile(curator_path), f"The script {curator_path} does not exist."
    assert os.access(curator_path, os.X_OK), f"The script {curator_path} is not executable."

def test_curated_directory_contents():
    curated_dir = "/home/user/curated"
    assert os.path.isdir(curated_dir), f"Directory {curated_dir} does not exist."

    expected_files = {
        "verified_initial_valid.zip",
        "verified_system_backup_1.tar.gz",
        "verified_data_package.zip"
    }

    actual_files = set(os.listdir(curated_dir))

    missing = expected_files - actual_files
    assert not missing, f"Missing files in curated directory: {missing}"

    unexpected = actual_files - expected_files
    assert not unexpected, f"Unexpected files in curated directory: {unexpected}"

def test_quarantine_directory_contents():
    quarantine_dir = "/home/user/quarantine"
    assert os.path.isdir(quarantine_dir), f"Directory {quarantine_dir} does not exist."

    expected_files = {
        "Bad Start.zip",
        "Broken Archive.tar.gz"
    }

    actual_files = set(os.listdir(quarantine_dir))

    missing = expected_files - actual_files
    assert not missing, f"Missing files in quarantine directory: {missing}"

    unexpected = actual_files - expected_files
    assert not unexpected, f"Unexpected files in quarantine directory: {unexpected}"

def test_dropzone_is_empty_of_target_files():
    dropzone_dir = "/home/user/dropzone"
    assert os.path.isdir(dropzone_dir), f"Directory {dropzone_dir} does not exist."

    files_in_dropzone = os.listdir(dropzone_dir)

    # SHUTDOWN should be deleted
    assert "SHUTDOWN" not in files_in_dropzone, "SHUTDOWN file was not deleted from dropzone."

    # The original files should have been moved
    original_files = {
        "Initial Valid.zip",
        "Bad Start.zip",
        "System Backup 1.tar.gz",
        "Broken Archive.tar.gz",
        "Data package.zip"
    }

    remaining = original_files.intersection(files_in_dropzone)
    assert not remaining, f"Files were left in the dropzone: {remaining}"

def test_no_tmp_files_in_curated():
    curated_dir = "/home/user/curated"
    if os.path.isdir(curated_dir):
        tmp_files = [f for f in os.listdir(curated_dir) if f.endswith(".tmp")]
        assert not tmp_files, f"Found unexpected .tmp files in curated directory: {tmp_files}"