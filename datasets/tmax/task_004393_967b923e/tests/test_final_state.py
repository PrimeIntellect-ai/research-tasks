# test_final_state.py

import os
import subprocess
import pytest

def test_binary_exists():
    binary_path = "/home/user/ws_filter/ws_filter"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist. Did you run make?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_allowed_log_contents():
    log_path = "/home/user/allowed.log"
    assert os.path.isfile(log_path), f"Output file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["101", "104", "105", "106"]
    assert lines == expected, f"Contents of {log_path} are incorrect. Expected {expected}, got {lines}."

def test_makefile_fixed():
    makefile_path = "/home/user/ws_filter/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "semver.o" in content, "Makefile does not appear to link semver.o."

def test_build_success():
    # Run make clean and make to ensure it builds correctly
    base_dir = "/home/user/ws_filter"

    # Run make clean
    subprocess.run(["make", "clean"], cwd=base_dir, capture_output=True)

    # Run make
    result = subprocess.run(["make"], cwd=base_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with error:\n{result.stderr}"

    binary_path = os.path.join(base_dir, "ws_filter")
    assert os.path.isfile(binary_path), "make succeeded but ws_filter binary was not created."