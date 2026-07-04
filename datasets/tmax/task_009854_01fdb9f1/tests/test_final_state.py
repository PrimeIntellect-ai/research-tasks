# test_final_state.py

import os
import pytest

def test_diagnostics_file_exists():
    assert os.path.isfile("/home/user/diagnostics.txt"), "/home/user/diagnostics.txt does not exist. Did you create the report?"

def test_diagnostics_content():
    with open("/home/user/diagnostics.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 non-empty lines in diagnostics.txt, found {len(lines)}."

    assert lines[0] == "DIAG_TOKEN_X7K9M2Q4", f"Line 1 of diagnostics.txt is incorrect. Expected 'DIAG_TOKEN_X7K9M2Q4', got '{lines[0]}'."
    assert lines[1] == "73", f"Line 2 of diagnostics.txt is incorrect. Expected '73', got '{lines[1]}'."

def test_venv_exists():
    assert os.path.isdir("/home/user/venv"), "The virtual environment directory /home/user/venv does not exist."
    assert os.path.isfile("/home/user/venv/bin/python") or os.path.isfile("/home/user/venv/bin/python3"), "Python executable not found in /home/user/venv/bin/."

def test_generated_files_exist():
    assert os.path.isfile("/home/user/app/memory.dmp"), "/home/user/app/memory.dmp does not exist. Did the script run successfully?"
    assert os.path.isfile("/home/user/app/output_data.json"), "/home/user/app/output_data.json does not exist. Did the script run successfully?"