# test_final_state.py

import os
import re
import pytest

def test_solution_file_exists():
    """Check if solution.txt exists."""
    assert os.path.isfile("/home/user/nightly/solution.txt"), "The file /home/user/nightly/solution.txt does not exist."

def test_solution_content():
    """Check if solution.txt contains the correct calculated value."""
    with open("/home/user/nightly/solution.txt", "r") as f:
        content = f.read().strip()

    # We expect a value around 200000000.00 or 200000001.22 due to floating point math
    # Accept regex 20000000[01]\.[0-9]{2}
    pattern = r"^20000000[01]\.[0-9]{2}$"
    assert re.match(pattern, content), f"The content of solution.txt ('{content}') does not match the expected format or value."

def test_process_executable_exists():
    """Check if the recompiled process executable exists."""
    assert os.path.isfile("/home/user/nightly/process"), "The recompiled executable /home/user/nightly/process does not exist."
    assert os.access("/home/user/nightly/process", os.X_OK), "The file /home/user/nightly/process is not executable."