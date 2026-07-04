# test_final_state.py

import os
import hashlib
import pytest

def test_backup_created_correctly():
    backup_file = '/home/user/docs_backup/api/v1/auth.md'
    assert os.path.isfile(backup_file), f"Backup file {backup_file} was not created."
    with open(backup_file, 'r') as f:
        content = f.read().strip()
    assert content == "Auth details for [COMPANY_NAME].", f"Backup file content is incorrect: {content}"

def test_zip_slip_prevention():
    # These files should not exist if zip slip was prevented
    malicious_files = [
        '/home/user/malicious.txt',
        '/home/user/system_overwrite.txt'
    ]
    for m_file in malicious_files:
        assert not os.path.exists(m_file), f"Security failure: {m_file} was created outside the target directory."

def test_rebranding_and_updates():
    expected_contents = {
        '/home/user/docs_target/api/v1/auth.md': "Updated auth details for AcmeCorp. Token required.",
        '/home/user/docs_target/api/v1/intro.md': "Welcome to AcmeCorp API v1.",
        '/home/user/docs_target/guides/admin.md': "New admin guide for AcmeCorp.",
        '/home/user/docs_target/guides/user.md': "User guide for AcmeCorp product.",
        '/home/user/docs_target/api/v2/new.md': "New admin guide for AcmeCorp."
    }

    for file_path, expected_text in expected_contents.items():
        assert os.path.isfile(file_path), f"Expected file {file_path} is missing."
        with open(file_path, 'r') as f:
            content = f.read().strip()
        assert content == expected_text, f"Content of {file_path} is incorrect. Expected '{expected_text}', got '{content}'."

def test_final_manifest_correctness():
    manifest_path = '/home/user/final_manifest.txt'
    target_dir = '/home/user/docs_target'

    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    # Compute the expected manifest
    expected_lines = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            expected_lines.append(f"{sha256.hexdigest()}  {file_path}")

    expected_lines.sort()
    expected_manifest_content = "\n".join(expected_lines) + "\n"

    with open(manifest_path, 'r') as f:
        actual_manifest_content = f.read()

    assert actual_manifest_content == expected_manifest_content, "The final manifest does not match the expected sorted sha256sum output."