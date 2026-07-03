# test_final_state.py

import os
import pytest

OUTPUT_FILE = '/home/user/shortest_path.txt'
EXPECTED_PATH = 'Nexus_Global,Delta_Inc,Apex_Solutions'

def test_output_file_exists():
    """Test that the shortest_path.txt file exists."""
    assert os.path.exists(OUTPUT_FILE), f"Output file missing at {OUTPUT_FILE}"
    assert os.path.isfile(OUTPUT_FILE), f"Path {OUTPUT_FILE} is not a file"

def test_output_file_content():
    """Test that the output file contains the correct shortest path."""
    assert os.path.exists(OUTPUT_FILE), "Cannot check content, file is missing."

    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == EXPECTED_PATH, (
        f"Incorrect path found in {OUTPUT_FILE}.\n"
        f"Expected: '{EXPECTED_PATH}'\n"
        f"Got: '{content}'"
    )