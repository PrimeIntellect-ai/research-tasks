# test_final_state.py

import os
import re
import pytest

def test_success_log_exists_and_correct():
    log_file = '/home/user/success.log'
    assert os.path.isfile(log_file), f"Expected output file {log_file} does not exist. Did you run the script and redirect output?"

    with open(log_file, 'r') as f:
        content = f.read()

    assert "/home/user/data/file1.txt: Hello from file1" in content, "Missing expected output for file1.txt in success.log"
    assert "/home/user/data/file 2.txt: Hello from file 2" in content, "Missing expected output for 'file 2.txt' in success.log. Did you fix the quoting issue in run_all.sh?"

def test_run_all_sh_fixed():
    script_file = '/home/user/project/run_all.sh'
    assert os.path.isfile(script_file), f"{script_file} is missing"

    with open(script_file, 'r') as f:
        content = f.read()

    # Check if $file is quoted
    assert re.search(r'"\$file"|\$\{file\}|"\$\{file\}"', content) is not None, "run_all.sh does not seem to have $file properly quoted to handle spaces."

def test_processor_cpp_fixed():
    cpp_file = '/home/user/project/processor.cpp'
    assert os.path.isfile(cpp_file), f"{cpp_file} is missing"

    with open(cpp_file, 'r') as f:
        content = f.read()

    # Check for retry logic
    assert re.search(r'retries\s*(==|>=|>)\s*(3|2)', content) is not None, "processor.cpp does not seem to check if retries == 3."
    assert "Error: Could not read" in content, "processor.cpp does not print the required error message."
    assert "cerr" in content, "processor.cpp does not print the error to standard error."