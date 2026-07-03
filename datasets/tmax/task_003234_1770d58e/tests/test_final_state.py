# test_final_state.py

import os
import re

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Expected result file not found at {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "7.00", f"Expected result to be '7.00', but got '{content}'"

def test_process_code_fixes():
    process_path = "/home/user/process.py"
    assert os.path.isfile(process_path), f"Expected script not found at {process_path}"

    with open(process_path, "r") as f:
        content = f.read()

    # Check for iteration limit fix (should contain 100)
    assert re.search(r'\b100\b', content), "Could not find iteration limit of 100 in process.py"

    # Check for utf-16le decoding fix
    assert "utf-16le" in content.lower() or "utf_16_le" in content.lower(), "Could not find 'utf-16le' decoding logic in process.py"