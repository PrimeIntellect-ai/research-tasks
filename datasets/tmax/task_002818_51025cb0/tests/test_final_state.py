# test_final_state.py

import os
import pytest

def test_fixture_c_exists_and_contains_mmap():
    fixture_path = "/home/user/test_fixture.c"
    assert os.path.isfile(fixture_path), f"File {fixture_path} does not exist."

    with open(fixture_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    assert "mmap" in content, f"File {fixture_path} does not contain 'mmap' as required."

def test_output_txt_exists_and_correct():
    output_path = "/home/user/test_output.txt"
    assert os.path.isfile(output_path), f"File {output_path} does not exist."

    with open(output_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()

    expected_content = "1B 3D 3F 34 2E 02"
    assert content == expected_content, f"Contents of {output_path} are incorrect. Expected '{expected_content}', got '{content}'."