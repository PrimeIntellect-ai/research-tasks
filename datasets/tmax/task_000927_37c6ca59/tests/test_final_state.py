# test_final_state.py

import os
import json
import pytest

def test_file_permissions():
    """Verify that the permissions of the files are correct after remediation."""
    files_and_perms = {
        "/home/user/project/processor.py": 0o775,
        "/home/user/project/helper.py": 0o755,
        "/home/user/project/network.py": 0o666,
        "/home/user/project/utils.py": 0o775,
    }

    for filepath, expected_perm in files_and_perms.items():
        assert os.path.isfile(filepath), f"File {filepath} does not exist."

        # Check permissions
        stat = os.stat(filepath)
        actual_perm = stat.st_mode & 0o777
        assert actual_perm == expected_perm, (
            f"File {filepath} has incorrect permissions. "
            f"Expected {oct(expected_perm)}, got {oct(actual_perm)}."
        )

def test_remediated_files_json():
    """Verify that the JSON output file contains exactly the remediated files."""
    json_path = "/home/user/remediated_files.json"
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Data in {json_path} should be a JSON array."

    expected_files = {
        "/home/user/project/processor.py",
        "/home/user/project/utils.py"
    }

    actual_files = set(data)
    assert actual_files == expected_files, (
        f"Incorrect files listed in {json_path}. "
        f"Expected {expected_files}, got {actual_files}."
    )
    assert len(data) == len(expected_files), (
        f"The array in {json_path} contains duplicate or extra entries."
    )