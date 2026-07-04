# test_final_state.py
import os
import json
import stat
import pytest

def test_report_json_exists_and_correct():
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), f"The report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    expected_data = {
        "clean.txt": "safe",
        "traversal.txt": "malicious",
        "xss.txt": "malicious",
        "hidden.enc": "malicious"
    }

    assert report_data == expected_data, f"The content of {report_path} does not match the expected report mapping."

def test_file_permissions():
    expected_permissions = {
        "clean.txt": 0o644,
        "traversal.txt": 0o000,
        "xss.txt": 0o000,
        "hidden.enc": 0o000
    }

    for filename, expected_mode in expected_permissions.items():
        filepath = os.path.join('/home/user/uploads', filename)
        assert os.path.isfile(filepath), f"The file {filepath} is missing."

        file_stat = os.stat(filepath)
        actual_mode = stat.S_IMODE(file_stat.st_mode)

        assert actual_mode == expected_mode, f"The permissions for {filename} are incorrect. Expected {oct(expected_mode)}, got {oct(actual_mode)}."