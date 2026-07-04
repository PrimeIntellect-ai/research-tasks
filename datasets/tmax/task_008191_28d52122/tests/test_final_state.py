# test_final_state.py
import os
import pytest

ROOTS_FILE = "/home/user/roots.txt"
CYCLES_FILE = "/home/user/cycles.txt"
SCRIPT_FILE = "/home/user/analyze_graph.sh"

EXPECTED_ROOTS = [
    "extract_inventory",
    "extract_orders",
    "extract_users",
    "job_A"
]

EXPECTED_CYCLES = [
    "job_B",
    "job_C",
    "job_X",
    "job_Y",
    "job_Z"
]

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_FILE), f"Script missing at {SCRIPT_FILE}"
    assert os.access(SCRIPT_FILE, os.X_OK), f"Script at {SCRIPT_FILE} is not executable"

def test_roots_file_content():
    """Test that the roots.txt file contains the correct root jobs."""
    assert os.path.isfile(ROOTS_FILE), f"Roots file missing at {ROOTS_FILE}"

    with open(ROOTS_FILE, "r") as f:
        content = f.read().strip().splitlines()

    assert content == EXPECTED_ROOTS, f"Roots file content is incorrect. Expected {EXPECTED_ROOTS}, got {content}"

def test_cycles_file_content():
    """Test that the cycles.txt file contains the correct cyclic jobs."""
    assert os.path.isfile(CYCLES_FILE), f"Cycles file missing at {CYCLES_FILE}"

    with open(CYCLES_FILE, "r") as f:
        content = f.read().strip().splitlines()

    assert content == EXPECTED_CYCLES, f"Cycles file content is incorrect. Expected {EXPECTED_CYCLES}, got {content}"