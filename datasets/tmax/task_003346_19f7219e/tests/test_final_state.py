# test_final_state.py

import os
import re

def test_source_code_exists_and_contains_rename():
    cpp_file = "/home/user/data_indexer.cpp"
    assert os.path.isfile(cpp_file), f"Source file {cpp_file} does not exist."

    with open(cpp_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert re.search(r'\brename\b', content), "The source code does not appear to contain logic for atomic writes (e.g., 'rename' or 'std::rename')."

def test_executable_exists():
    exe_file = "/home/user/data_indexer"
    assert os.path.isfile(exe_file), f"Executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_index_csv_content():
    csv_file = "/home/user/index.csv"
    assert os.path.isfile(csv_file), f"Output file {csv_file} does not exist."

    with open(csv_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "DS_099,/home/user/data/other/3.json",
        "DS_100,/home/user/data/1.json"
    ]

    assert lines == expected_lines, f"Content of {csv_file} does not match expected output. Got: {lines}"