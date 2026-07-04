# test_final_state.py

import os
import pytest

def test_extracted_backup_key_exists():
    """Test that the backup key was successfully extracted from the zip file."""
    extracted_dir = "/home/user/extracted"

    # The zip was created with an absolute path, so it might extract with the full path
    # or just the filename depending on how the student extracted it.
    possible_paths = [
        os.path.join(extracted_dir, "backup_key.pem"),
        os.path.join(extracted_dir, "home", "user", "backup_key.pem")
    ]

    found = any(os.path.exists(p) and os.path.isfile(p) for p in possible_paths)

    if not found:
        # Check recursively in case it was extracted differently
        for root, dirs, files in os.walk(extracted_dir):
            if "backup_key.pem" in files:
                found = True
                break

    assert found, "The backup_key.pem file was not found in /home/user/extracted/ or its subdirectories."

def test_cert_info_format_and_content():
    """Test that cert_info.txt contains the correct Issuer Organization and Serial Number."""
    cert_info_path = "/home/user/cert_info.txt"
    assert os.path.exists(cert_info_path), f"The file {cert_info_path} does not exist."
    assert os.path.isfile(cert_info_path), f"{cert_info_path} is not a file."

    with open(cert_info_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert len(lines) >= 2, f"{cert_info_path} must contain at least two lines."

    expected_org = "Global Security Inc"
    expected_serial = "01abcdef"

    assert lines[0] == expected_org, f"Line 1 of {cert_info_path} is incorrect. Expected '{expected_org}', got '{lines[0]}'."
    assert lines[1].lower() == expected_serial, f"Line 2 of {cert_info_path} is incorrect. Expected '{expected_serial}', got '{lines[1]}'."

def test_rotated_master_key_exists_and_correct():
    """Test that the command injection was successful and copied the hidden master key."""
    rotated_key_path = "/home/user/rotated_master_key.txt"
    hidden_key_path = "/home/user/.hidden_master_key"

    assert os.path.exists(rotated_key_path), f"The file {rotated_key_path} does not exist. The exploit may have failed."
    assert os.path.isfile(rotated_key_path), f"{rotated_key_path} is not a file."

    assert os.path.exists(hidden_key_path), f"The original hidden key {hidden_key_path} is missing."

    with open(hidden_key_path, "r") as f:
        expected_content = f.read().strip()

    with open(rotated_key_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"The content of {rotated_key_path} does not match the hidden master key."