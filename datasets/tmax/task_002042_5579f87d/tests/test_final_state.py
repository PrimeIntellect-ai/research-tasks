# test_final_state.py

import os
import hashlib
import pytest

def test_clean_unique_file_exists():
    assert os.path.isfile("/home/user/clean_unique.txt"), "The output file /home/user/clean_unique.txt is missing."

def test_clean_unique_file_contents():
    expected_lines = [
        "16e3ba63f5cba239ed7e54f9a5d3f2ec20ebaa9dfd08269e96eab445f1b1b017:apple pie",
        "b493d48364afe44d11c0165cf470a4164d1e2609911ef998be868d46ade3de4e:banana",
        "335f60cd19aab624d62ddb03b22b4cb102eb9de3b13eb06f9e54a6db2462eaf9:café moca"
    ]

    with open("/home/user/clean_unique.txt", "r", encoding="utf-8") as f:
        content = f.read()

    assert content.endswith("\n"), "The file /home/user/clean_unique.txt must end with a newline."

    lines = content.splitlines()
    assert len(lines) == 3, f"Expected 3 lines in /home/user/clean_unique.txt, but found {len(lines)}."

    for i, expected_line in enumerate(expected_lines):
        assert lines[i] == expected_line, f"Line {i+1} does not match expected output.\nExpected: {expected_line}\nActual: {lines[i]}"