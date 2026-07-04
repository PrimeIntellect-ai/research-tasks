# test_final_state.py

import os
import pytest
import re

def test_output_file_exists():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file {path} was not created."

def test_output_file_contents():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file {path} was not created."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/login 57.7",
        "/data 55",
        "/calc 14",
        "/auth 2.5"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output.txt, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."

def test_parser_fixed():
    path = "/home/user/proxy_analyzer/parser.cpp"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # The original bug used string_view on a local variable.
    # We should ensure that the string_view bug is removed or fixed.
    # A correct implementation would just push `word` directly to `entry.tokens` as a string.
    assert "std::string_view(word)" not in content, "The dangling reference bug using std::string_view(word) is still present in parser.cpp."

def test_evaluator_implemented():
    path = "/home/user/proxy_analyzer/evaluator.cpp"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check if stack operations or a stack data structure is used
    has_stack_include = "<stack>" in content
    has_push = "push" in content
    has_pop = "pop" in content
    has_vector_back = "back" in content and "pop_back" in content

    assert (has_stack_include and has_push and has_pop) or (has_push and has_vector_back), \
        "evaluator.cpp does not appear to implement a stack-based algorithm (missing push/pop or stack operations)."

    # Check for math operators
    assert "+" in content and "-" in content and "*" in content and "/" in content, \
        "evaluator.cpp does not seem to implement all required arithmetic operators (+, -, *, /)."