# test_final_state.py

import os
import json
import zipfile
import pytest

def test_summary_json_exists_and_correct():
    """Test that summary.json exists and contains the correct mapping."""
    summary_path = "/home/user/summary.json"
    assert os.path.exists(summary_path), f"The file {summary_path} is missing."
    assert os.path.isfile(summary_path), f"{summary_path} should be a file."

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {summary_path} does not contain valid JSON.")

    expected_data = {
        "job_002": "3h 45m",
        "job_004": "2h 10m"
    }

    assert data == expected_data, f"The contents of {summary_path} are incorrect. Expected {expected_data}, but got {data}."

def test_valid_gcodes_zip_exists_and_correct():
    """Test that valid_gcodes.zip exists, is valid, and contains the correct renamed gcode files."""
    zip_path = "/home/user/valid_gcodes.zip"
    assert os.path.exists(zip_path), f"The file {zip_path} is missing."
    assert os.path.isfile(zip_path), f"{zip_path} should be a file."
    assert zipfile.is_zipfile(zip_path), f"{zip_path} is not a valid zip archive."

    expected_files = {
        "job_002_model.gcode": "; LAYER_COUNT: 150",
        "job_004_model.gcode": "; LAYER_COUNT: 120"
    }

    with zipfile.ZipFile(zip_path, "r") as z:
        zip_contents = set(z.namelist())
        expected_names = set(expected_files.keys())

        assert zip_contents == expected_names, f"The zip archive {zip_path} contains incorrect files. Expected {expected_names}, but got {zip_contents}."

        for filename, expected_content in expected_files.items():
            with z.open(filename) as f:
                content = f.read().decode('utf-8')
                assert expected_content in content, f"The file {filename} inside the zip archive does not contain the expected layer count. Expected to find '{expected_content}'."