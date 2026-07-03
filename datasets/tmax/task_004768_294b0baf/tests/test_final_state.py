# test_final_state.py

import os
import pytest

def test_cleaned_logs_exist_and_correct_lines():
    cleaned_dir = "/home/user/cleaned_logs"

    expected_files = {
        "node1.log": 50,
        "node2.log": 150,
        "node3.log": 0
    }

    # Check that directory exists
    assert os.path.isdir(cleaned_dir), f"Directory {cleaned_dir} is missing."

    # Check exactly these files exist in the directory
    actual_files = set(os.listdir(cleaned_dir))
    assert actual_files == set(expected_files.keys()), f"Expected files {set(expected_files.keys())} but found {actual_files} in {cleaned_dir}."

    # Check line counts and content
    for filename, expected_lines in expected_files.items():
        filepath = os.path.join(cleaned_dir, filename)
        assert os.path.isfile(filepath), f"File {filepath} is missing."

        with open(filepath, "r") as f:
            lines = f.readlines()

        assert len(lines) == expected_lines, f"Expected {expected_lines} lines in {filename}, but found {len(lines)}."

        # Ensure no [TRACE] or [DEBUG] in the remaining lines
        for line_num, line in enumerate(lines, 1):
            assert "[TRACE]" not in line, f"Found [TRACE] in {filename} at line {line_num}."
            assert "[DEBUG]" not in line, f"Found [DEBUG] in {filename} at line {line_num}."

def test_inventory_file_content():
    inventory_path = "/home/user/inventory.txt"
    assert os.path.isfile(inventory_path), f"Inventory file {inventory_path} is missing."

    expected_lines = {
        "node1.log,50",
        "node2.log,150",
        "node3.log,0"
    }

    with open(inventory_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert set(actual_lines) == expected_lines, f"Expected inventory lines {expected_lines}, but found {set(actual_lines)}."
    assert len(actual_lines) == 3, f"Expected exactly 3 lines in inventory.txt, but found {len(actual_lines)}."