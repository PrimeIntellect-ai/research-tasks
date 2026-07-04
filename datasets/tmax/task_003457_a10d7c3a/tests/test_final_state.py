# test_final_state.py
import os
import json

def test_result_json_exists_and_correct():
    result_path = '/home/user/result.json'
    assert os.path.exists(result_path), f"The file {result_path} does not exist."
    assert os.path.isfile(result_path), f"{result_path} is not a file."

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{result_path} does not contain valid JSON."

    expected_data = {
        "backup_evil.csv": [
            ["id", "name"],
            ["1", "alice"]
        ],
        "backup_safe1.csv": [
            ["id", "name"],
            ["2", "bob"]
        ],
        "backup_passwd.csv": [
            ["id", "name"],
            ["3", "charlie"]
        ]
    }

    assert data == expected_data, f"The contents of {result_path} do not match the expected output. Got: {data}"

def test_extracted_files_renamed_and_flattened():
    extracted_dir = '/home/user/extracted'
    assert os.path.exists(extracted_dir), f"The directory {extracted_dir} does not exist."

    files_in_extracted = set(os.listdir(extracted_dir))
    expected_files = {"backup_evil.csv", "backup_safe1.csv", "backup_passwd.csv"}

    # Check that the expected files are present
    for expected_file in expected_files:
        assert expected_file in files_in_extracted, f"Expected file {expected_file} is missing from {extracted_dir}."

    # Check that no un-prefixed files or directories exist
    for f in files_in_extracted:
        assert f.startswith("backup_") and f.endswith(".csv"), f"Found unexpected file {f} in {extracted_dir}."

def test_no_directory_traversal():
    # Check that malicious files did not escape to parent directories
    assert not os.path.exists('/home/user/evil.csv'), "Path traversal occurred: /home/user/evil.csv was created."
    assert not os.path.exists('/evil.csv'), "Path traversal occurred: /evil.csv was created."
    assert not os.path.exists('/passwd.csv'), "Path traversal occurred: /passwd.csv was created."
    assert not os.path.exists('/home/passwd.csv'), "Path traversal occurred: /home/passwd.csv was created."