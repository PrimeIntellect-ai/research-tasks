# test_final_state.py

import os
import pytest

def test_source_and_executable_exist():
    source_file = "/home/user/organize_archives.cpp"
    executable_file = "/home/user/organize_archives"

    assert os.path.isfile(source_file), f"C++ source file {source_file} is missing."
    assert os.path.isfile(executable_file), f"Compiled executable {executable_file} is missing."
    assert os.access(executable_file, os.X_OK), f"File {executable_file} is not executable."

def test_verified_zips_exist():
    expected_verified = [
        "/home/user/project_backups/module_a/backup1_verified.zip",
        "/home/user/project_backups/module_b/backup2_verified.zip",
        "/home/user/project_backups/module_b/deep_dir/backup3_verified.zip"
    ]
    for f in expected_verified:
        assert os.path.isfile(f), f"Expected verified zip file {f} is missing."

def test_corrupt_zips_exist():
    expected_corrupt = [
        "/home/user/project_backups/module_a/backup_broken1_corrupt.zip",
        "/home/user/project_backups/module_b/deep_dir/backup_broken2_corrupt.zip"
    ]
    for f in expected_corrupt:
        assert os.path.isfile(f), f"Expected corrupt zip file {f} is missing."

def test_original_zips_removed():
    original_files = [
        "/home/user/project_backups/module_a/backup1.zip",
        "/home/user/project_backups/module_b/backup2.zip",
        "/home/user/project_backups/module_b/deep_dir/backup3.zip",
        "/home/user/project_backups/module_a/backup_broken1.zip",
        "/home/user/project_backups/module_b/deep_dir/backup_broken2.zip"
    ]
    for f in original_files:
        assert not os.path.exists(f), f"Original zip file {f} should have been renamed/removed."

def test_no_extra_zips():
    expected_all = {
        "/home/user/project_backups/module_a/backup1_verified.zip",
        "/home/user/project_backups/module_b/backup2_verified.zip",
        "/home/user/project_backups/module_b/deep_dir/backup3_verified.zip",
        "/home/user/project_backups/module_a/backup_broken1_corrupt.zip",
        "/home/user/project_backups/module_b/deep_dir/backup_broken2_corrupt.zip"
    }

    found_zips = set()
    for root, _, files in os.walk("/home/user/project_backups"):
        for file in files:
            if file.endswith(".zip"):
                found_zips.add(os.path.join(root, file))

    extra_zips = found_zips - expected_all
    assert not extra_zips, f"Found unexpected zip files: {extra_zips}"