# test_final_state.py
import os
import json
import pytest

def test_config_fixed_exists_and_correct():
    path = "/home/user/project_files/config_fixed.json"
    assert os.path.isfile(path), f"The output file was not created at {path}. Did the Rust client run successfully and save the output?"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {path} does not contain valid JSON.")

    expected_data = {
      "version": "1.0",
      "name": "organized_project",
      "files": [
        "new_file1.txt",
        "new_file2.txt"
      ]
    }

    assert data == expected_data, f"The patched content in {path} does not match the expected output. Make sure the Rust client applies the diff correctly."