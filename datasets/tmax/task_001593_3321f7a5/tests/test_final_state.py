# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/find_match.sh"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing: {SCRIPT_PATH}"

def test_find_match_u100():
    result = subprocess.run(
        ["bash", SCRIPT_PATH, "U100"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    output = result.stdout.strip()
    assert output == "C4", f"Expected output 'C4' for U100, but got '{output}'"

def test_find_match_u102():
    result = subprocess.run(
        ["bash", SCRIPT_PATH, "U102"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    output = result.stdout.strip()
    assert output == "C5", f"Expected output 'C5' for U102, but got '{output}'"

def test_find_match_u101():
    result = subprocess.run(
        ["bash", SCRIPT_PATH, "U101"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    output = result.stdout.strip()
    assert output == "C4", f"Expected output 'C4' for U101, but got '{output}'"