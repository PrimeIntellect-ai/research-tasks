# test_final_state.py

import os
import stat
import pytest

SCRIPT_PATH = "/home/user/analyze.sh"
OUTPUT_PATH = "/home/user/top_papers.txt"

EXPECTED_OUTPUT = """Alice|Beta|7
Carol|Eta|6
Carol|Zeta|6
Bob|Epsilon|5
David|Theta|1
"""

def test_script_exists_and_executable():
    """Test if the analyze.sh script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"Script {SCRIPT_PATH} is not executable."

def test_output_file_exists():
    """Test if the top_papers.txt output file exists."""
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

def test_output_contents():
    """Test if the contents of top_papers.txt exactly match the expected output."""
    with open(OUTPUT_PATH, "r") as f:
        content = f.read().strip()

    expected_stripped = EXPECTED_OUTPUT.strip()

    assert content == expected_stripped, \
        f"Output file contents do not match expected.\nExpected:\n{expected_stripped}\nGot:\n{content}"