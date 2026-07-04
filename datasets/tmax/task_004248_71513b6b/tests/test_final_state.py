# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    """Verify the bash script was created at the requested location."""
    script_path = "/home/user/consolidate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_symlink_exists_and_correct():
    """Verify the symlink points to the correct target."""
    symlink_path = "/home/user/current_config"
    target_path = "/home/user/output/latest_config.json"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    assert os.readlink(symlink_path) == target_path, f"Symlink {symlink_path} does not point to {target_path}."

def test_json_content_and_size():
    """Verify the JSON output is correct and minified."""
    target_path = "/home/user/output/latest_config.json"

    assert os.path.isfile(target_path), f"Output file {target_path} does not exist."

    expected = {
        "host": "db.example.com",
        "port": "5432",
        "user": "admin",
        "pass": "secret123",
        "retries": "3"
    }

    with open(target_path, 'r') as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"File {target_path} does not contain valid JSON.")

    assert data == expected, f"JSON content {data} does not match expected {expected}."

    file_size = len(content)
    threshold = 90
    assert file_size <= threshold, f"File size is {file_size} bytes, expected <= {threshold} bytes. The JSON is not sufficiently minified."