# test_final_state.py

import os
import pytest

def test_migration_targets_file_exists():
    assert os.path.isfile('/home/user/migration_targets.txt'), "The output file /home/user/migration_targets.txt was not created."

def test_migration_targets_contents():
    with open('/home/user/migration_targets.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        'src/app.py',
        'src/config.py'
    ]

    assert lines == expected_lines, f"The contents of /home/user/migration_targets.txt do not match the expected output. Got: {lines}"

def test_original_files_unmodified():
    # Check that original files still exist
    expected_files = [
        '/home/user/legacy_project/src/app.py',
        '/home/user/legacy_project/src/utils.py',
        '/home/user/legacy_project/src/helper.py',
        '/home/user/legacy_project/src/config.py',
        '/home/user/legacy_project/src/math.py',
        '/home/user/legacy_project/checksums.md5'
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"The original file {file_path} is missing. It should not have been modified or deleted."