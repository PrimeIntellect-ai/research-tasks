# test_final_state.py

import os
import pytest

def test_c_source_exists():
    assert os.path.isfile('/home/user/config_tracker.c'), "The C source file /home/user/config_tracker.c does not exist."

def test_executable_exists():
    executable_path = '/home/user/config_tracker'
    assert os.path.isfile(executable_path), f"The executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_output_file_exists_and_content():
    output_path = '/home/user/output.txt'
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_output = """srv-münchen (11 chars): 50 bytes, avg: 50.00
srv-londres (11 chars): 120 bytes, avg: 120.00
srv-münchen (11 chars): 60 bytes, avg: 55.00
srv-münchen (11 chars): 70 bytes, avg: 60.00
srv-münchen (11 chars): 80 bytes, avg: 70.00
srv-東京 (6 chars): 200 bytes, avg: 200.00
srv-서울 (6 chars): 150 bytes, avg: 150.00
srv-東京 (6 chars): 300 bytes, avg: 250.00
srv-서울 (6 chars): 250 bytes, avg: 200.00
srv-東京 (6 chars): 100 bytes, avg: 200.00
srv-東京 (6 chars): 400 bytes, avg: 266.67"""

    assert content == expected_output, f"The content of {output_path} does not match the expected output. Found:\n{content}"