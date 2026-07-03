# test_final_state.py

import os
import json
import pytest

def test_app_json_extracted_correctly():
    path = "/home/user/extracted_configs/app.json"
    assert os.path.isfile(path), f"Expected file {path} was not found."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert data == {"env": "production"}, f"Content of {path} is incorrect. Got {data}"

def test_db_config_json_extracted_correctly():
    path = "/home/user/extracted_configs/db/config.json"
    assert os.path.isfile(path), f"Expected file {path} was not found."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert data == {"port": "5432"}, f"Content of {path} is incorrect. Got {data}"

def test_zip_slip_mitigated():
    forbidden_paths = [
        "/home/user/pwned_sys.json",
        "/home/user/pwned_sys.csv",
        "/home/user/extracted_configs/../pwned_sys.json",
        "/home/user/extracted_configs/../pwned_sys.csv"
    ]

    for path in forbidden_paths:
        normalized_path = os.path.normpath(path)
        assert not os.path.exists(normalized_path), f"Zip slip vulnerability detected: {normalized_path} should not exist."

def test_no_tmp_files_left():
    base_dir = "/home/user/extracted_configs"
    assert os.path.isdir(base_dir), f"Directory {base_dir} does not exist."

    tmp_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".tmp"):
                tmp_files.append(os.path.join(root, file))

    assert not tmp_files, f"Temporary files were left behind: {tmp_files}"