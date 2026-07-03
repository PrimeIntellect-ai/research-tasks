# test_final_state.py
import os
import re

def test_source_code_fixed():
    source_path = "/home/user/signal_processor.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, "r") as f:
        content = f.read()

    assert "reduction" in content, "The source code does not contain the 'reduction' clause in the OpenMP directive."

def test_executable_exists():
    exec_path = "/home/user/signal_processor"
    assert os.path.isfile(exec_path), f"Executable {exec_path} is missing. Did you compile the code?"
    assert os.access(exec_path, os.X_OK), f"File {exec_path} is not executable."

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing. Did you run the program and save the output?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected_value = "4702500.000000"
    assert content == expected_value, f"Expected result to be {expected_value}, but got {content}."