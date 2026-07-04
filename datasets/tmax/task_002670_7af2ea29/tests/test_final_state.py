# test_final_state.py
import os
import pytest

def test_author_citations_output():
    tsv_path = "/home/user/author_citations.tsv"
    assert os.path.isfile(tsv_path), f"Output file {tsv_path} does not exist."

    expected_lines = [
        "Dave Davis\tAlice Smith\t2",
        "Alice Smith\tBob Jones\t1",
        "Alice Smith\tCharlie Brown\t1",
        "Dave Davis\tCharlie Brown\t1"
    ]

    with open(tsv_path, 'r', encoding='utf-8') as f:
        actual_lines = [line.strip('\r\n') for line in f if line.strip('\r\n')]

    assert actual_lines == expected_lines, (
        f"Contents of {tsv_path} do not match expected output.\n"
        f"Expected:\n{expected_lines}\n"
        f"Actual:\n{actual_lines}"
    )

def test_extract_cpp_exists():
    cpp_path = "/home/user/extract.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."