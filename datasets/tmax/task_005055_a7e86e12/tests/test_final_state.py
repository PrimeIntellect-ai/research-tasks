# test_final_state.py

import os
import re

def test_result_file_exists_and_correct():
    result_path = "/home/user/math_proj/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did you run the script?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected = "Max Length: 143, Number: 327"
    assert content == expected, f"Expected '{expected}' in {result_path}, but got '{content}'"

def test_run_analysis_fixed():
    script_path = "/home/user/math_proj/run_analysis.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "math_v1.sh" not in content, "run_analysis.sh should no longer source the broken math_v1.sh library."
    assert "math_v2.sh" in content, "run_analysis.sh must still source math_v2.sh."

def test_math_v2_optimized():
    lib_path = "/home/user/math_proj/lib/math_v2.sh"
    assert os.path.isfile(lib_path), f"File {lib_path} is missing."

    with open(lib_path, "r") as f:
        content = f.read()

    # Check that expr is no longer used
    assert "expr " not in content, "The collatz function in math_v2.sh is still using the slow 'expr' command. Use Bash native arithmetic (e.g., $((...)))."

    # Check that collatz is still defined
    assert "collatz" in content, "The collatz function must still be defined in math_v2.sh."