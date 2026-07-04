# test_final_state.py

import os
import json
import re
import pytest

def test_math_api_fixed():
    """Verify that math_api.py is secured and the memory leak is fixed."""
    math_api_path = "/home/user/math_api.py"
    assert os.path.isfile(math_api_path), f"File {math_api_path} is missing."

    with open(math_api_path, "r") as f:
        content = f.read()

    assert "eval(" not in content, "math_api.py still contains the unsafe eval() function."
    assert "ast" in content, "math_api.py does not use the ast module for safe evaluation."

    # Check for bounded history constraint (e.g., maxlen=10, pop(0), [-10:])
    history_bounded = re.search(r'maxlen\s*=\s*10|pop\(0\)|\[-10:\]|del\s+history\[0\]|history\.pop\(0\)', content) or \
                      re.search(r'len\(history\)\s*>\s*10', content) or \
                      re.search(r'len\(history\)\s*>=\s*10', content) or \
                      re.search(r'len\(history\)\s*==\s*11', content)

    assert history_bounded, "math_api.py does not appear to bound the history list to 10 items."

def test_test_client_exists():
    """Verify that test_client.py was created."""
    test_client_path = "/home/user/test_client.py"
    assert os.path.isfile(test_client_path), f"File {test_client_path} is missing."

def test_test_output_json():
    """Verify the test output JSON matches the expected values."""
    output_path = "/home/user/test_output.json"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} is not valid JSON.")

    # Values might be strings or numbers depending on serialization, cast to string for robust comparison
    str_data = [str(x) for x in data]
    expected = ["42", "25.0", "72", "36", "ERROR"]

    assert str_data == expected, f"Expected {expected}, but got {str_data} in {output_path}."

def test_mprof_dat():
    """Verify that the memory profile data file exists and is valid."""
    mprof_path = "/home/user/mprof.dat"
    assert os.path.isfile(mprof_path), f"File {mprof_path} is missing."

    with open(mprof_path, "r") as f:
        first_line = f.readline()

    assert first_line.startswith("CMDLINE"), f"{mprof_path} does not appear to be a valid mprof data file."
    assert "math_api.py" in first_line, f"{mprof_path} was not run on math_api.py."