# test_final_state.py

import os
import re
import pytest

def test_evaluator_cpp_exists():
    """Test that the C++ program was created."""
    cpp_path = "/home/user/evaluator.cpp"
    assert os.path.isfile(cpp_path), f"Failed: C++ source file not found at {cpp_path}"
    assert os.path.getsize(cpp_path) > 0, f"Failed: C++ source file is empty at {cpp_path}"

def test_result_txt_metric():
    """Test that the result.txt contains the correct evaluated number within the threshold."""
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Failed: result file not found at {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    match = re.search(r'-?\d+(\.\d+)?', content)
    assert match is not None, f"Failed: No numerical value found in {result_path}. Content: '{content}'"

    value = float(match.group(0))
    target = 463.25
    error = abs(value - target)

    assert error <= 0.1, f"Failed: output {value} is outside threshold (error = {error}, expected <= 0.1)"