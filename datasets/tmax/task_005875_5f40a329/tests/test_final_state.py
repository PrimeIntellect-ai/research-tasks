# test_final_state.py

import os
import pytest
import re

APP_DIR = "/home/user/app"
PROCESSOR_PY = os.path.join(APP_DIR, "processor.py")
SOLUTION_TXT = "/home/user/solution.txt"

def test_processor_py_fixed():
    assert os.path.isfile(PROCESSOR_PY), f"File {PROCESSOR_PY} does not exist."
    with open(PROCESSOR_PY, "r") as f:
        content = f.read()

    assert "def process_x" in content, "process_x function missing in processor.py"
    assert "def process_y" in content, "process_y function missing in processor.py"

    # Check process_x lock order
    x_idx = content.find("def process_x")
    y_idx = content.find("def process_y")

    # If y is before x, adjust boundaries
    if y_idx < x_idx:
        y_content = content[y_idx:x_idx]
    else:
        y_content = content[y_idx:]

    lock_a_idx = y_content.find("with lock_a:")
    lock_b_idx = y_content.find("with lock_b:")

    assert lock_a_idx != -1, "lock_a not found in process_y"
    assert lock_b_idx != -1, "lock_b not found in process_y"
    assert lock_a_idx < lock_b_idx, "process_y must acquire lock_a before lock_b to fix the deadlock."

def test_solution_txt_correct():
    assert os.path.isfile(SOLUTION_TXT), f"File {SOLUTION_TXT} does not exist."

    with open(SOLUTION_TXT, "r") as f:
        content = f.read().strip()

    # The expected output is specifically these two transaction IDs in alphabetical order
    expected = "TXN_33B2E1, TXN_88A9F0"

    assert content == expected, f"Expected solution.txt to contain exactly '{expected}', but got '{content}'"