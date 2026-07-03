# test_final_state.py
import os
import zipfile
import pytest

def test_script_exists_and_uses_flock():
    script_path = '/home/user/update_configs.py'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    with open(script_path, 'r') as f:
        code = f.read()
    assert 'fcntl.flock' in code, "Script does not use fcntl.flock as required."

def test_backup_zip_exists_and_contents():
    zip_path = '/home/user/pre_update_backup.zip'
    assert os.path.exists(zip_path), f"Backup zip {zip_path} does not exist."

    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()

        # Check expected files are in the zip
        assert 'serviceA/config.ini' in names, "serviceA/config.ini missing from backup zip."
        assert 'serviceB/nested/settings.ini' in names, "serviceB/nested/settings.ini missing from backup zip."

        # Check unmodified file is NOT in the zip
        assert 'serviceC/config.ini' not in names, "serviceC/config.ini should not be in backup zip because it didn't need modification."

        # Check original content in the zip
        content_A = z.read('serviceA/config.ini').decode('utf-8')
        assert '[auth_v1]' in content_A, "Original [auth_v1] missing in backed up serviceA/config.ini."
        assert 'token_expiry = 3600' in content_A, "Original token_expiry missing in backed up serviceA/config.ini."

        content_B = z.read('serviceB/nested/settings.ini').decode('utf-8')
        assert '[auth_v1]' in content_B, "Original [auth_v1] missing in backed up serviceB/nested/settings.ini."
        assert 'token_expiry = 3600' in content_B, "Original token_expiry missing in backed up serviceB/nested/settings.ini."

def test_updated_files_content():
    # Check serviceA
    file_path_A = '/home/user/app_configs/serviceA/config.ini'
    assert os.path.exists(file_path_A), f"File {file_path_A} missing."
    with open(file_path_A, 'r') as f:
        content_A = f.read()
    assert '[auth_v2]' in content_A, f"[auth_v2] not found in {file_path_A}."
    assert 'token_expiry = 86400' in content_A, f"token_expiry = 86400 not found in {file_path_A}."
    assert '[auth_v1]' not in content_A, f"[auth_v1] should be replaced in {file_path_A}."

    # Check serviceB
    file_path_B = '/home/user/app_configs/serviceB/nested/settings.ini'
    assert os.path.exists(file_path_B), f"File {file_path_B} missing."
    with open(file_path_B, 'r') as f:
        content_B = f.read()
    assert '[auth_v2]' in content_B, f"[auth_v2] not found in {file_path_B}."
    assert 'token_expiry = 86400' in content_B, f"token_expiry = 86400 not found in {file_path_B}."
    assert '[auth_v1]' not in content_B, f"[auth_v1] should be replaced in {file_path_B}."

def test_unmodified_file_content():
    # Check serviceC remains unchanged
    file_path_C = '/home/user/app_configs/serviceC/config.ini'
    assert os.path.exists(file_path_C), f"File {file_path_C} missing."
    with open(file_path_C, 'r') as f:
        content_C = f.read()
    assert '[auth_v2]' in content_C, f"Expected [auth_v2] in {file_path_C}."
    assert 'token_expiry = 86400' in content_C, f"Expected token_expiry = 86400 in {file_path_C}."