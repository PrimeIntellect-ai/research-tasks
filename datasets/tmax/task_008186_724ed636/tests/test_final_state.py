# test_final_state.py

import os
import re
import pytest

def test_processed_output():
    output_path = "/home/user/processed_output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} was not created. Did the program run successfully?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "900000", f"Expected processed_output.txt to contain '900000', but got '{content}'. The sum is incorrect or the program failed to process all valid files."

def test_corrupted_files_output():
    corrupted_path = "/home/user/corrupted_files.txt"
    assert os.path.isfile(corrupted_path), f"Output file {corrupted_path} was not created. Did the program catch the panic and write the corrupted file path?"

    with open(corrupted_path, "r") as f:
        content = f.read().strip()

    expected = "/home/user/data/bad log.csv"
    assert content == expected, f"Expected corrupted_files.txt to contain '{expected}', but got '{content}'."

def test_memory_leak_fixed():
    process_go_path = "/home/user/logprocessor/processor/process.go"
    assert os.path.isfile(process_go_path), f"Source file {process_go_path} is missing."

    with open(process_go_path, "r") as f:
        content = f.read()

    # Check that MemoryLeakCache is not being assigned to
    assignment_match = re.search(r'MemoryLeakCache\[.+?\]\s*=', content)
    assert not assignment_match, "MemoryLeakCache is still being populated in process.go, meaning the memory leak is not fixed."