# test_final_state.py

import os
import pytest

C_FILE_PATH = '/home/user/extractor.c'
EXEC_FILE_PATH = '/home/user/extractor'
CSV_FILE_PATH = '/home/user/valid_relays.csv'

def test_c_file_exists():
    """Test that the C source file exists."""
    assert os.path.isfile(C_FILE_PATH), f"C source file missing at {C_FILE_PATH}"

def test_executable_exists():
    """Test that the compiled executable exists."""
    assert os.path.isfile(EXEC_FILE_PATH), f"Executable missing at {EXEC_FILE_PATH}"
    assert os.access(EXEC_FILE_PATH, os.X_OK), f"File at {EXEC_FILE_PATH} is not executable"

def test_csv_output():
    """Test that the output CSV exists and contains the correct data."""
    assert os.path.isfile(CSV_FILE_PATH), f"CSV output file missing at {CSV_FILE_PATH}"

    expected_content = """start,relay,end,path_power
NodeP,NodeQ,NodeR,75.0
NodeB,NodeC,NodeD,70.0
NodeA,NodeB,NodeC,60.5"""

    with open(CSV_FILE_PATH, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content.strip(), (
        f"CSV content does not match expected output.\n"
        f"Expected:\n{expected_content}\n\nGot:\n{actual_content}"
    )