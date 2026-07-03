# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_script_exists_and_executable():
    """Test if /home/user/aggregate.sh exists and is executable."""
    script_path = "/home/user/aggregate.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_script_uses_flock():
    """Test if /home/user/aggregate.sh contains the flock command."""
    script_path = "/home/user/aggregate.sh"
    with open(script_path, "r") as f:
        content = f.read()
    assert "flock" in content, f"Script {script_path} does not seem to use 'flock'."
    assert "/home/user/summary.lock" in content, f"Script {script_path} does not seem to lock '/home/user/summary.lock'."

def test_script_execution_and_output():
    """Test running the script and verify the output in /home/user/summary.csv."""
    script_path = "/home/user/aggregate.sh"
    summary_path = "/home/user/summary.csv"

    # Clean up summary.csv if it exists to ensure a fresh test
    if os.path.exists(summary_path):
        os.remove(summary_path)

    datasets = [
        "/home/user/datasets/sample1.json",
        "/home/user/datasets/sample2.csv",
        "/home/user/datasets/sample3.xml"
    ]

    # Run the script for each dataset
    for dataset in datasets:
        result = subprocess.run([script_path, dataset], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed when processing {dataset}. Error: {result.stderr}"

    # Check if summary.csv was created
    assert os.path.exists(summary_path), f"{summary_path} was not created."

    # Read and verify the contents of summary.csv
    with open(summary_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "sample1.json,GenomeDB,5000",
        "sample2.csv,ClimateData,12500",
        "sample3.xml,OceanTemps,8900"
    }

    actual_lines = set(lines)

    missing = expected_lines - actual_lines
    unexpected = actual_lines - expected_lines

    assert actual_lines == expected_lines, f"Summary contents incorrect. Missing: {missing}, Unexpected: {unexpected}"