# test_final_state.py

import os
import pytest

def test_uptime_result_exists():
    """
    Verify that the result file was created.
    """
    result_file = "/home/user/uptime_result.txt"
    assert os.path.isfile(result_file), f"The result file {result_file} is missing."

def test_uptime_result_content():
    """
    Verify that the result file contains the correct numerical total uptime.
    """
    result_file = "/home/user/uptime_result.txt"
    if not os.path.isfile(result_file):
        pytest.fail(f"Cannot check content because {result_file} is missing.")

    with open(result_file, 'r') as f:
        content = f.read().strip()

    assert content == "16200", f"Expected the uptime result to be '16200', but got '{content}'."