# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

SCRIPT_PATH = "/home/user/find_path.sh"

def test_script_exists_and_executable():
    """Check if the find_path.sh script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script at {SCRIPT_PATH} is not executable"

def test_shortest_path_101_105():
    """Check if the script correctly finds the shortest path between 101 and 105."""
    result = subprocess.run([SCRIPT_PATH, "101", "105"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script exited with non-zero status: {result.stderr}"

    output = result.stdout.strip()
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON. Got: {output}")

    assert data == [101, 108, 105], f"Expected path [101, 108, 105], but got {data}"

def test_unreachable_path_105_101():
    """Check if the script correctly handles unreachable paths."""
    result = subprocess.run([SCRIPT_PATH, "105", "101"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script exited with non-zero status: {result.stderr}"

    output = result.stdout.strip()
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON. Got: {output}")

    assert data == [], f"Expected empty array [] for unreachable path, but got {data}"

def test_dead_end_path_101_110():
    """Check if the script correctly finds a path to a dead end."""
    result = subprocess.run([SCRIPT_PATH, "101", "110"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script exited with non-zero status: {result.stderr}"

    output = result.stdout.strip()
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON. Got: {output}")

    assert data == [101, 109, 110], f"Expected path [101, 109, 110], but got {data}"