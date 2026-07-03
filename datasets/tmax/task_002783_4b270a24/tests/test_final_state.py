# test_final_state.py
import os
import json
import subprocess
import pytest
import stat

def test_migrate_script_exists():
    script_path = "/home/user/data_project/migrate.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

def test_setup_ci_script_exists_and_executable():
    script_path = "/home/user/data_project/setup_ci.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_migrate_execution_and_output():
    script_path = "/home/user/data_project/migrate.py"
    raw_dir = "/home/user/data_project/raw"
    processed_dir = "/home/user/data_project/processed"

    # Run the migrate script
    result = subprocess.run(["python3", script_path, raw_dir, processed_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"migrate.py failed to run. Stderr: {result.stderr}"

    # Check outputs
    file1_path = os.path.join(processed_dir, "2021", "A001.json")
    file2_path = os.path.join(processed_dir, "2022", "B022.json")

    assert os.path.exists(file1_path), f"Expected output file {file1_path} not found."
    assert os.path.exists(file2_path), f"Expected output file {file2_path} not found."

    with open(file1_path, 'r') as f:
        data1 = json.load(f)
    assert data1 == {"record_id": "A001", "first_name": "Alice", "last_name": "Smith", "year": 2021}, "Content of A001.json is incorrect."

    with open(file2_path, 'r') as f:
        data2 = json.load(f)
    assert data2 == {"record_id": "B022", "first_name": "Bob", "last_name": "Jones", "year": 2022}, "Content of B022.json is incorrect."

def test_setup_ci_execution_and_output():
    script_path = "/home/user/data_project/setup_ci.sh"

    # Run the bash script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"setup_ci.sh failed to run. Stderr: {result.stderr}"

    pipeline_path = "/home/user/data_project/.github/workflows/pipeline.yml"
    assert os.path.exists(pipeline_path), f"Pipeline file {pipeline_path} was not created."

    with open(pipeline_path, 'r') as f:
        content = f.read()

    required_strings = [
        "process-data",
        "ubuntu-latest",
        "migrate.py",
        "cross-compile-tools",
        "make build ARCH=arm64"
    ]

    for req in required_strings:
        assert req in content, f"Pipeline file is missing required string: '{req}'"