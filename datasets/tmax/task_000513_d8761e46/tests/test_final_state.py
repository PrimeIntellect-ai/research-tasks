# test_final_state.py

import os
import re
import pytest

def test_cleaned_small_txt_content():
    path = "/home/user/cleaned_small.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    expected = "hello world this is a test data cleaning is fun 123"
    assert content.strip() == expected, f"Content of {path} does not match the expected cleaned output. Got: {content!r}"

def test_times_txt_exists_and_format():
    path = "/home/user/times.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 30, f"Expected exactly 30 lines in {path}, got {len(lines)}."
    for i, line in enumerate(lines):
        assert line.isdigit(), f"Line {i+1} in {path} is not an integer: {line!r}"

def test_benchmark_stats_format():
    path = "/home/user/benchmark_stats.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    pattern = r"^Mean: \d+\.\d{2} ms, 95% CI: \[\d+\.\d{2} ms, \d+\.\d{2} ms\]$"
    assert re.match(pattern, content), f"Content of {path} does not match the expected format. Got: {content!r}"

def test_executables_and_scripts_exist():
    expected_files = [
        "/home/user/tokenizer.c",
        "/home/user/tokenizer",
        "/home/user/benchmark.sh",
        "/home/user/stats.c",
        "/home/user/stats"
    ]
    for path in expected_files:
        assert os.path.isfile(path), f"Expected file/executable {path} does not exist."
        if not path.endswith(".c") and not path.endswith(".txt"):
            assert os.access(path, os.X_OK), f"Expected {path} to be executable."