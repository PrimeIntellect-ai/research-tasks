# test_final_state.py

import os
import pytest

def test_verified_files_moved():
    expected_files = [
        "/home/user/repo/x86_64/bin/app_main.bin",
        "/home/user/repo/aarch64/modules/network.ko"
    ]
    for filepath in expected_files:
        assert os.path.exists(filepath), f"Expected verified file was not moved to correct target path: {filepath}"

def test_unverified_files_not_moved():
    unexpected_file = "/home/user/repo/armv7/lib/helper.so"
    assert not os.path.exists(unexpected_file), f"Corrupted file should not have been moved to {unexpected_file}"

def test_summary_file_content():
    summary_path = "/home/user/curator_summary.txt"
    assert os.path.exists(summary_path), f"Summary file is missing at {summary_path}"

    with open(summary_path, "r") as f:
        content = f.read().strip()

    expected_content = "Successfully curated: 2 artifacts"
    assert content == expected_content, f"Summary file content is incorrect. Expected '{expected_content}', got '{content}'"

def test_original_verified_files_removed():
    unexpected_incoming_files = [
        "/home/user/incoming/raw_001.dat",
        "/home/user/incoming/raw_003.dat"
    ]
    for filepath in unexpected_incoming_files:
        assert not os.path.exists(filepath), f"Verified file {filepath} was copied instead of moved (or not moved at all)."