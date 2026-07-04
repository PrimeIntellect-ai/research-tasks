# test_final_state.py
import os
import subprocess
import pytest

SOLUTION_DIR = "/home/user/solution"
CRASH_INPUT = os.path.join(SOLUTION_DIR, "crash_input.bin")
FAULT_FUNC = os.path.join(SOLUTION_DIR, "fault_func.txt")
SAFE_PARSER = os.path.join(SOLUTION_DIR, "safe_parser.c")
FIXED_SERVER = os.path.join(SOLUTION_DIR, "fixed_server")

def test_crash_input_bin():
    assert os.path.isfile(CRASH_INPUT), f"Missing {CRASH_INPUT}"
    with open(CRASH_INPUT, "rb") as f:
        content = f.read()
    expected = b"USER:" + b"A"*64 + b"\n"
    assert content == expected, f"Content of {CRASH_INPUT} is incorrect. Expected {expected}, got {content}"

def test_fault_func_txt():
    assert os.path.isfile(FAULT_FUNC), f"Missing {FAULT_FUNC}"
    with open(FAULT_FUNC, "r") as f:
        content = f.read().strip()
    assert content == "extract_field", f"Content of {FAULT_FUNC} is incorrect. Expected 'extract_field', got '{content}'"

def test_safe_parser_c():
    assert os.path.isfile(SAFE_PARSER), f"Missing {SAFE_PARSER}"
    with open(SAFE_PARSER, "r") as f:
        content = f.read()
    assert "parse_and_process" in content, f"Function 'parse_and_process' not found in {SAFE_PARSER}"

def test_fixed_server_exists_and_executable():
    assert os.path.isfile(FIXED_SERVER), f"Missing {FIXED_SERVER}"
    assert os.access(FIXED_SERVER, os.X_OK), f"{FIXED_SERVER} is not executable"

def test_fixed_server_behavior():
    # Test with crash_input.bin
    with open(CRASH_INPUT, "rb") as f:
        crash_data = f.read()

    proc = subprocess.run([FIXED_SERVER], input=crash_data, capture_output=True)
    assert proc.returncode == 0, f"{FIXED_SERVER} crashed or returned non-zero exit code on crash input"

    # Test with valid input
    valid_input = b"DATA:short_value\n"
    proc_valid = subprocess.run([FIXED_SERVER], input=valid_input, capture_output=True)
    assert proc_valid.returncode == 0, f"{FIXED_SERVER} returned non-zero exit code on valid input"
    assert b"short_value" in proc_valid.stdout, f"{FIXED_SERVER} did not process valid input correctly"

def test_fixed_server_truncation():
    # Verify that the safe parser truncates the output to 31 characters to prevent overflow
    long_input = b"TEST:" + b"B"*50 + b"\n"
    proc = subprocess.run([FIXED_SERVER], input=long_input, capture_output=True)
    assert proc.returncode == 0, f"{FIXED_SERVER} crashed on long input"
    # The output should contain at most 31 'B's (or 31 chars total including \n depending on implementation)
    # The requirement says "truncates the copied data to 31 characters"
    assert b"B"*32 not in proc.stdout, f"{FIXED_SERVER} did not truncate the output to 31 characters"