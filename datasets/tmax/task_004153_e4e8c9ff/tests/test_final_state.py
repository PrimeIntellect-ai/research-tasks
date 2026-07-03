# test_final_state.py

import os
import pytest

def test_emerging_terms_file_exists():
    path = "/home/user/emerging_terms.txt"
    assert os.path.isfile(path), f"The file {path} does not exist."

def test_emerging_terms_content():
    path = "/home/user/emerging_terms.txt"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_terms = ["floob", "widget", "zarkon"]

    assert lines == expected_terms, (
        f"Contents of {path} do not match the expected output. "
        f"Expected {expected_terms}, but got {lines}."
    )