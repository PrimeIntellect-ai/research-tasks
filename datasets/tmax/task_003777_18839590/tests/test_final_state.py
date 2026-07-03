# test_final_state.py

import os
import re
import subprocess
import pytest

def test_perf_log():
    log_path = "/home/user/perf.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    # Check for the first expression
    expr1_pattern = r"\[EXPR\]\s*10\*\(\s*5\s*\+\s*5\s*\)\s*\[RESULT\]\s*100\s*\[TIME_US\]\s*\d+"
    assert re.search(expr1_pattern, content), "Log file does not contain the expected entry for '10*(5+5)'."

    # Check for the second expression
    expr2_pattern = r"\[EXPR\]\s*\(\s*100\s*/\s*10\s*\)\s*-\s*2\s*\[RESULT\]\s*8\s*\[TIME_US\]\s*\d+"
    assert re.search(expr2_pattern, content), "Log file does not contain the expected entry for '(100/10)-2'."

def test_rust_binary_exists():
    bin_path = "/home/user/rust_proj/target/debug/rust_proj"
    assert os.path.isfile(bin_path), f"Rust binary {bin_path} does not exist. Did the compilation succeed?"
    assert os.access(bin_path, os.X_OK), f"Rust binary {bin_path} is not executable."

def test_rust_binary_output():
    bin_path = "/home/user/rust_proj/target/debug/rust_proj"
    assert os.path.isfile(bin_path), f"Rust binary {bin_path} does not exist."

    result = subprocess.run([bin_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running the Rust binary failed with return code {result.returncode}."

    expected_output = "Values are: 100 and 8"
    assert expected_output in result.stdout, f"Expected output '{expected_output}' not found in binary output: {result.stdout}"