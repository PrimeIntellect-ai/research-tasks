# test_final_state.py

import os
import gzip
import json
import re
import pytest

def test_fatal_log_content():
    source_file = "/home/user/raw_data/system_logs.gz"
    dest_file = "/home/user/project_xray/fatal.log"

    assert os.path.isfile(source_file), f"Source file {source_file} is missing."
    assert os.path.isfile(dest_file), f"Destination file {dest_file} was not created."

    expected_lines = []
    with gzip.open(source_file, 'rt') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("project") == "x-ray" and data.get("level") == "FATAL":
                    expected_lines.append(line)
            except json.JSONDecodeError:
                continue

    with open(dest_file, 'r') as f:
        actual_lines = f.readlines()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {dest_file}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {dest_file} does not match the expected raw JSON string."

def test_go_script_atomic_rename():
    script_file = "/home/user/parse_logs.go"
    assert os.path.isfile(script_file), f"Go script {script_file} is missing."

    with open(script_file, 'r') as f:
        content = f.read()

    # Check for atomic rename requirement
    assert re.search(r'\b(os|syscall)\.Rename\b', content), f"The Go script {script_file} does not appear to use os.Rename or syscall.Rename for atomic writing."