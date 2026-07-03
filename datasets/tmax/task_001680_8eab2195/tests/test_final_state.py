# test_final_state.py

import os
import subprocess
import pytest

def test_resolution_file_content():
    path = "/home/user/resolution.txt"
    assert os.path.isfile(path), f"Resolution file missing at {path}."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content in ["9900", "9900.0"], f"Incorrect resolution value in {path}. Expected 9900 or 9900.0, got '{content}'."

def test_test_boundary_conditions_exists():
    path = "/home/user/incident-1042/src/main.rs"
    assert os.path.isfile(path), f"Source file missing at {path}."

    with open(path, "r") as f:
        content = f.read()

    assert "fn test_boundary_conditions" in content, "The test function 'test_boundary_conditions' is missing in main.rs."

def test_cargo_test_passes():
    project_dir = "/home/user/incident-1042"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} does not exist."

    result = subprocess.run(
        ["cargo", "test", "--quiet"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"`cargo test` failed with output:\n{result.stdout}\n{result.stderr}"