# test_final_state.py
import os
import pytest

C_FILE_PATH = "/home/user/query_graph.c"
EXEC_PATH = "/home/user/query_graph"
OUTPUT_PATH = "/home/user/output.csv"

EXPECTED_CSV_CONTENT = """Author_Name,Dataset_Name
Alice Smith,GraphDB-1M
Bob Jones,GraphDB-1M
Charlie Brown,ImageNet-Mini
"""

def test_c_source_exists():
    assert os.path.isfile(C_FILE_PATH), f"C source file {C_FILE_PATH} is missing."

def test_executable_exists():
    assert os.path.isfile(EXEC_PATH), f"Compiled executable {EXEC_PATH} is missing."
    assert os.access(EXEC_PATH, os.X_OK), f"File {EXEC_PATH} is not executable."

def test_output_csv_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."

def test_output_csv_content():
    with open(OUTPUT_PATH, "r") as f:
        content = f.read()

    # Strip trailing newlines for comparison, but ensure it's structurally correct
    assert content.strip() == EXPECTED_CSV_CONTENT.strip(), "The contents of output.csv do not match the expected output."

    # Check exact header
    lines = content.strip().split('\n')
    assert lines[0] == "Author_Name,Dataset_Name", "The CSV header is incorrect."