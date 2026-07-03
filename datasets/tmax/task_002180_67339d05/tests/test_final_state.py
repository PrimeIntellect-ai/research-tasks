# test_final_state.py

import os
import json
import pytest

def test_security_report_json():
    """Test that the security_report.json file exists and contains the correct malicious paths."""
    report_path = '/home/user/security_report.json'
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_data = {
        "user_profiles.zip": ["../../../home/user/.bashrc"],
        "core_sys.zip": ["/etc/shadow"]
    }

    assert report_data == expected_data, f"Contents of {report_path} do not match the expected security report."

def test_extracted_files_exist():
    """Test that the safe files were extracted and CSV was converted."""
    extracted_dir = '/home/user/extracted'

    # Expected files
    assert os.path.isfile(os.path.join(extracted_dir, 'users.json')), "users.json was not found in the extracted directory."
    assert os.path.isfile(os.path.join(extracted_dir, 'readme.txt')), "readme.txt was not found in the extracted directory."
    assert os.path.isfile(os.path.join(extracted_dir, 'config.bin')), "config.bin was not found in the extracted directory."

def test_extracted_users_json_content():
    """Test that users.json contains the correct parsed CSV data."""
    users_json_path = '/home/user/extracted/users.json'

    with open(users_json_path, 'r') as f:
        try:
            users_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {users_json_path} is not valid JSON.")

    expected_users = [
        {"id": "1", "username": "admin", "role": "superuser"},
        {"id": "2", "username": "bob", "role": "editor"}
    ]

    assert users_data == expected_users, f"Contents of {users_json_path} do not match expected parsed CSV data."

def test_extracted_readme_txt_content():
    """Test that readme.txt contains the correct text."""
    readme_path = '/home/user/extracted/readme.txt'
    with open(readme_path, 'r') as f:
        content = f.read()
    assert content == 'Backup instructions.', "Contents of readme.txt are incorrect."

def test_extracted_config_bin_content():
    """Test that config.bin contains the correct binary data."""
    config_path = '/home/user/extracted/config.bin'
    with open(config_path, 'rb') as f:
        content = f.read()
    assert content == b'\x00\x01\x02\x03\x04', "Contents of config.bin are incorrect."

def test_users_csv_removed():
    """Test that the original users.csv file was deleted after conversion."""
    csv_path = '/home/user/extracted/users.csv'
    assert not os.path.exists(csv_path), "The original users.csv file was not deleted."

def test_malicious_files_not_extracted():
    """Test that files from malicious zips were not extracted."""
    extracted_dir = '/home/user/extracted'
    malicious_files = [
        'safe_file.txt',
        'normal_dir/path.txt',
        'normal_dir',
        '.bashrc',
        'shadow'
    ]

    for m_file in malicious_files:
        path = os.path.join(extracted_dir, m_file)
        assert not os.path.exists(path), f"Malicious or associated file {m_file} was incorrectly extracted."