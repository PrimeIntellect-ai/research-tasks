# test_final_state.py

import os
import pytest

def test_safe_extract_directory_exists_and_contains_correct_files():
    extract_dir = "/home/user/config_update/safe_extract"
    assert os.path.exists(extract_dir), f"Directory {extract_dir} does not exist. Did you extract the files?"
    assert os.path.isdir(extract_dir), f"{extract_dir} is not a directory."

    expected_files = {"service_a.conf", "service_b.conf", "new_service.conf"}
    actual_files = set(os.listdir(extract_dir))

    for ef in expected_files:
        assert ef in actual_files, f"Expected file {ef} is missing from {extract_dir}."

def test_no_malicious_files_extracted():
    extract_dir = "/home/user/config_update/safe_extract"
    assert os.path.exists(extract_dir), f"Directory {extract_dir} does not exist."

    actual_files = set(os.listdir(extract_dir))
    expected_files = {"service_a.conf", "service_b.conf", "new_service.conf"}

    unexpected_files = actual_files - expected_files
    assert not unexpected_files, f"Found unexpected files in {extract_dir}, which might indicate a Zip Slip vulnerability was not mitigated: {unexpected_files}"

    # Also check that malicious files didn't end up in parent directory
    parent_dir = "/home/user/config_update"
    parent_files = set(os.listdir(parent_dir))
    assert "evil_traversal.conf" not in parent_files, "Found 'evil_traversal.conf' in parent directory. Zip Slip mitigation failed."

    # Check absolute path extraction failure
    assert not os.path.exists("/absolute/evil.conf"), "Found '/absolute/evil.conf'. Zip Slip mitigation failed."

def test_differential_backup_list_correct():
    list_path = "/home/user/config_update/differential_backup.list"
    assert os.path.exists(list_path), f"File {list_path} does not exist. Did you generate the backup list?"
    assert os.path.isfile(list_path), f"{list_path} is not a file."

    with open(list_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/config_update/safe_extract/new_service.conf",
        "/home/user/config_update/safe_extract/service_b.conf"
    ]

    assert lines == expected_lines, f"Contents of {list_path} do not match the expected sorted list of changed/new files. Expected: {expected_lines}, Got: {lines}"