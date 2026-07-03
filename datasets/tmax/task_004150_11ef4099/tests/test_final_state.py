# test_final_state.py

import os
import json
import subprocess
import pytest

def test_build_index_script_exists_and_executable():
    script_path = "/home/user/build_index.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_build_index_execution_and_output():
    script_path = "/home/user/build_index.sh"
    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {script_path} failed with return code {result.returncode}.\nStderr: {result.stderr}"

    index_dir = "/home/user/backup_index"
    assert os.path.isdir(index_dir), f"Directory {index_dir} was not created."

    expected_symlinks = {
        "1000-A1.json": "A1.json",
        "1010-A2.json": "A2.json",
        "1020-A3.json": "A3.json",
        "2000-B1.json": "B1.json",
        "2010-B2.json": "B2.json",
        "2020-B3.json": "B3.json",
    }

    actual_files = os.listdir(index_dir)
    for symlink_name, target_name in expected_symlinks.items():
        assert symlink_name in actual_files, f"Expected symlink {symlink_name} not found in {index_dir}."

        symlink_path = os.path.join(index_dir, symlink_name)
        assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

        target_path = os.readlink(symlink_path)
        # The target should resolve to the correct file in /home/user/backups
        absolute_target = os.path.abspath(os.path.join(index_dir, target_path))
        expected_absolute_target = os.path.abspath(f"/home/user/backups/{target_name}")

        assert absolute_target == expected_absolute_target, f"Symlink {symlink_name} points to {absolute_target}, expected {expected_absolute_target}."

def test_get_chain_script_exists_and_executable():
    script_path = "/home/user/get_chain.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_get_chain_execution_and_output():
    script_path = "/home/user/get_chain.sh"
    # Execute the script with timestamp 2015
    result = subprocess.run([script_path, "2015"], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {script_path} 2015 failed with return code {result.returncode}.\nStderr: {result.stderr}"

    output_file = "/home/user/recovery_plan.json"
    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    with open(output_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} does not contain valid JSON.")

    expected_data = [
        {
            "id": "B1",
            "type": "full",
            "file": "backup_B1.tar.gz"
        },
        {
            "id": "B2",
            "type": "incremental",
            "file": "backup_B2.tar.gz"
        }
    ]

    assert data == expected_data, f"JSON content in {output_file} does not match the expected output. Got: {data}"