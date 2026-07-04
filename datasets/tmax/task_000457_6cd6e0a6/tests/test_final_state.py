# test_final_state.py
import os
import pytest

def test_import_ready_exists():
    path = "/home/user/import_ready.tsv"
    assert os.path.isfile(path), f"File {path} is missing. The pipeline did not create the expected output file."

def test_import_ready_content():
    path = "/home/user/import_ready.tsv"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip("\n") for line in f.readlines()]

    expected_lines = [
        "id\temail\trating\tcomment\tcum_rating",
        "101\t[REDACTED]\t5\tAbsolutely love it!\t5",
        "103\t[REDACTED]\t4\tSolid performance.\t9",
        '105\t[REDACTED]\t5\t"Perfect, no complaints"\t14',
        "106\t[REDACTED]\t2\tMeh.\t16"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} does not match expected output.\nExpected: {repr(expected)}\nActual:   {repr(actual)}"