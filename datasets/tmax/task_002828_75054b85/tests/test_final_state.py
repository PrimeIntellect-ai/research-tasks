# test_final_state.py

import os
import pytest

def test_safe_manifest_exists():
    safe_manifest_path = "/home/user/safe_manifest.txt"
    assert os.path.isfile(safe_manifest_path), f"The final manifest file {safe_manifest_path} is missing."

def test_safe_manifest_contents():
    safe_manifest_path = "/home/user/safe_manifest.txt"

    # Deriving the expected safe paths based on the rules
    expected_safe_paths = [
        "data/user_uploads/image.png",
        "data/config.json",
        "normal_file.txt",
        "sneaky..file.txt"
    ]

    if os.path.isfile(safe_manifest_path):
        with open(safe_manifest_path, "r") as f:
            content = f.read().splitlines()

        assert content == expected_safe_paths, (
            f"The contents of {safe_manifest_path} do not match the expected safe paths. "
            f"Expected: {expected_safe_paths}, but got: {content}"
        )

def test_temp_file_removed():
    tmp_manifest_path = "/home/user/safe_manifest.tmp"
    assert not os.path.exists(tmp_manifest_path), (
        f"The temporary file {tmp_manifest_path} still exists. "
        "It should have been atomically renamed to the final destination."
    )

def test_original_manifest_untouched():
    manifest_path = "/home/user/incremental_manifest.txt"
    assert os.path.isfile(manifest_path), f"The original manifest file {manifest_path} is missing."