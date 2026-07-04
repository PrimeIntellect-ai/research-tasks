# test_final_state.py
import os
import json
import pytest

def test_restore_staging_directory():
    staging_dir = "/home/user/restore_staging"
    assert os.path.isdir(staging_dir), f"Directory {staging_dir} does not exist. Did you extract the tarball to the correct location?"

    expected_files = ["file_a.dat", "file_b.dat", "file_c.dat", "file_d.dat"]
    for f in expected_files:
        file_path = os.path.join(staging_dir, f)
        assert os.path.isfile(file_path), f"Extracted file {file_path} is missing. The tarball was not extracted correctly."

def test_restore_report_json():
    report_path = "/home/user/restore_report.json"
    assert os.path.isfile(report_path), f"File {report_path} does not exist. Did you generate the final report?"

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not a valid JSON file.")

    expected_data = {
        "file_a.dat": "ok",
        "file_b.dat": "quota_exceeded",
        "file_c.dat": "quota_exceeded",
        "file_d.dat": "size_mismatch"
    }

    assert report_data == expected_data, f"The contents of {report_path} do not match the expected verification results. Got: {report_data}"