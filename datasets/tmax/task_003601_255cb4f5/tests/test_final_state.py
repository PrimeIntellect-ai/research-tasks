# test_final_state.py

import os
import pytest

def test_result_file_exists():
    """Verify that the result.txt file was created in the correct location."""
    result_path = "/home/user/qa_env/result.txt"
    assert os.path.isfile(result_path), f"The file {result_path} is missing. Did you save the output?"

def test_result_content():
    """Verify that the content of result.txt matches the expected Base64 encoded JSON response."""
    result_path = "/home/user/qa_env/result.txt"
    assert os.path.isfile(result_path), f"Cannot check content because {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected_base64 = "eyJzdW0iOiA0MC4wMDAwMDB9"

    assert content == expected_base64, (
        f"The content of {result_path} is incorrect.\n"
        f"Expected: {expected_base64}\n"
        f"Got: {content}\n"
        "Ensure the CMake linking, RPATH, Nginx proxy, and the request payload were all correct."
    )