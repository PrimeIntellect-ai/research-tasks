# test_final_state.py

import os
import tarfile
import pytest

BACKUP_V2_PATH = '/home/user/backup_v2.tar.gz'
PROJECT_DIR = '/home/user/project'

def test_backup_v2_exists():
    assert os.path.exists(BACKUP_V2_PATH), f"{BACKUP_V2_PATH} not found"

def test_backup_v2_contents():
    assert os.path.exists(BACKUP_V2_PATH), f"{BACKUP_V2_PATH} not found"

    with tarfile.open(BACKUP_V2_PATH, 'r:gz') as tar:
        names = tar.getnames()

        # Check required files
        assert 'app_diff.log' in names, "app_diff.log not found in the archive"
        assert 'data.bin' in names, "data.bin not found in the archive"

        # Check excluded files
        assert 'static.bin' not in names, "static.bin should not be in the archive (it is unchanged)"
        assert 'app.log' not in names, "app.log should not be in the archive (should be app_diff.log)"

def test_app_diff_log_content():
    assert os.path.exists(BACKUP_V2_PATH), f"{BACKUP_V2_PATH} not found"

    with tarfile.open(BACKUP_V2_PATH, 'r:gz') as tar:
        names = tar.getnames()
        if 'app_diff.log' not in names:
            pytest.fail("app_diff.log not found in the archive")

        f = tar.extractfile('app_diff.log')
        content = f.read().decode('utf-8').strip()
        expected = "2023-10-01 10:15:00 ERROR Out of memory\n2023-10-01 10:20:00 INFO Restarting"

        assert content == expected, f"app_diff.log content mismatch. Expected:\n{expected}\nGot:\n{content}"

def test_data_bin_content():
    assert os.path.exists(BACKUP_V2_PATH), f"{BACKUP_V2_PATH} not found"

    with tarfile.open(BACKUP_V2_PATH, 'r:gz') as tar:
        names = tar.getnames()
        if 'data.bin' not in names:
            pytest.fail("data.bin not found in the archive")

        f_data = tar.extractfile('data.bin')
        archived_data = f_data.read()

        curr_data_path = os.path.join(PROJECT_DIR, 'data.bin')
        assert os.path.exists(curr_data_path), f"{curr_data_path} is missing from the filesystem"

        with open(curr_data_path, 'rb') as curr_data:
            expected_data = curr_data.read()

        assert archived_data == expected_data, "data.bin in the archive does not match the current project data.bin"