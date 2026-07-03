# test_final_state.py
import os
import json
import tarfile
import pytest

def test_extracted_files_exist():
    base_dir = '/home/user/extracted_code'

    # Check for expected extracted files
    expected_files = [
        'python_scripts/main.py',
        'python_scripts/utils.py',
        'js_scripts/app.js'
    ]
    for f in expected_files:
        full_path = os.path.join(base_dir, f)
        assert os.path.isfile(full_path), f"Expected extracted file {full_path} is missing."

def test_ignored_files_do_not_exist():
    # The junk archive contains ignored.py, it should not be extracted
    junk_path = '/home/user/extracted_code/ignored.py'
    assert not os.path.exists(junk_path), f"File {junk_path} from junk archive should not have been extracted."

def test_index_json_conversion():
    json_path = '/home/user/extracted_code/index.json'
    assert os.path.isfile(json_path), f"{json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert isinstance(data, list), f"{json_path} should contain a JSON array."
    assert len(data) == 3, f"{json_path} should have exactly 3 entries."

    expected_entry = {"id": "1", "filename": "main.py", "language": "python"}
    assert expected_entry in data, f"Expected entry {expected_entry} not found in {json_path}."

def test_loc_summary():
    loc_path = '/home/user/loc_summary.txt'
    assert os.path.isfile(loc_path), f"{loc_path} is missing."

    with open(loc_path, 'r') as f:
        content = f.read().strip()

    assert content == "18", f"Expected LOC summary to be '18', got '{content}'."

def test_rearchived_dataset():
    tar_path = '/home/user/clean_dataset.tar'
    assert os.path.isfile(tar_path), f"{tar_path} is missing."

    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar file."

    with tarfile.open(tar_path, 'r') as tar:
        names = tar.getnames()

        # Check that the tar file contains the expected files
        # The exact paths in the tar might vary depending on how it was created
        # (e.g. 'extracted_code/index.json' vs './index.json' vs 'index.json')
        # We'll just check if the basenames exist in the paths
        has_index = any(name.endswith('index.json') for name in names)
        has_main = any(name.endswith('main.py') for name in names)

        assert has_index, f"index.json is missing from {tar_path}."
        assert has_main, f"main.py is missing from {tar_path}."