# test_final_state.py

import os
import stat
import pytest

def test_build_script_exists_and_executable():
    script_path = "/home/user/build_all.sh"
    assert os.path.exists(script_path), f"The script {script_path} was not generated."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_build_script_content():
    script_path = "/home/user/build_all.sh"
    assert os.path.exists(script_path), f"The script {script_path} was not generated."

    with open(script_path, "r") as f:
        content = f.read().strip()

    expected_content = """#!/bin/bash
echo "Building backend-go..."
cd /home/user/src/go-backend && make build
echo "Building cli-rust..."
cd /home/user/src/rust-cli && make build
echo "Building scripts-py..."
cd /home/user/src/py-scripts && make build
echo "Building aggregator-go..."
cd /home/user/src/go-agg && make build"""

    # Normalize line endings to avoid issues with \r\n vs \n
    normalized_content = "\n".join(line.strip() for line in content.splitlines() if line.strip())
    normalized_expected = "\n".join(line.strip() for line in expected_content.splitlines() if line.strip())

    assert normalized_content == normalized_expected, "The generated build_all.sh does not match the expected content and topological order."

def test_orchestrate_script_exists():
    script_path = "/home/user/orchestrate.py"
    assert os.path.exists(script_path), f"The Python script {script_path} was not created."
    assert os.path.isfile(script_path), f"{script_path} is not a file."