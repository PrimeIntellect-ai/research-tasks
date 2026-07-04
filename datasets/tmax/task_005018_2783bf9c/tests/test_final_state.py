# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/trace_lineage.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.path.isfile(script_path), f"Expected {script_path} to be a file"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_impacted_ds_005_output():
    output_path = "/home/user/impacted_DS_005.txt"
    assert os.path.exists(output_path), f"Missing output file: {output_path}"

    expected_datasets = [
        "DS_006",
        "DS_007",
        "DS_010",
        "DS_011",
        "DS_012",
        "DS_013",
        "DS_014"
    ]

    with open(output_path, "r") as f:
        content = f.read().splitlines()

    # Remove empty lines
    content = [line.strip() for line in content if line.strip()]

    assert content == expected_datasets, f"Contents of {output_path} are incorrect. Expected {expected_datasets}, got {content}"

def test_script_functionality_ds_001():
    script_path = "/home/user/trace_lineage.sh"
    deps_path = "/home/user/dataset_dependencies.tsv"

    # Run the script for DS_001
    result = subprocess.run(
        [script_path, "DS_001", deps_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. stderr: {result.stderr}"

    expected_datasets = [
        "DS_002",
        "DS_003",
        "DS_004"
    ]

    output = result.stdout.splitlines()
    output = [line.strip() for line in output if line.strip()]

    assert output == expected_datasets, f"Script output for DS_001 is incorrect. Expected {expected_datasets}, got {output}"