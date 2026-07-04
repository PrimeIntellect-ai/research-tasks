# test_final_state.py

import os
import pytest

DOCS_DIR = "/home/user/organized_docs"
CHUNKER_SCRIPT = "/home/user/chunker.py"

def test_chunker_script_exists():
    assert os.path.isfile(CHUNKER_SCRIPT), f"Chunker script missing at {CHUNKER_SCRIPT}"

def test_organized_docs_dir_exists():
    assert os.path.isdir(DOCS_DIR), f"Directory {DOCS_DIR} does not exist."

def test_section_files_exist_and_correct_length():
    for i in range(1, 26):
        filename = f"section_{i:03d}.md"
        filepath = os.path.join(DOCS_DIR, filename)
        assert os.path.isfile(filepath), f"File {filename} is missing in {DOCS_DIR}."

        with open(filepath, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 500, f"File {filename} has {len(lines)} lines, expected exactly 500."

def test_merged_index_correctness():
    index_path = os.path.join(DOCS_DIR, "merged_index.md")
    assert os.path.isfile(index_path), f"merged_index.md is missing in {DOCS_DIR}."

    with open(index_path, 'r') as f:
        index_lines = f.readlines()

    assert len(index_lines) == 25, f"merged_index.md has {len(index_lines)} lines, expected exactly 25."

    for i in range(1, 26):
        expected_entry = ((i - 1) * 100) + 1
        expected_line = f"# Document Entry {expected_entry}\n"
        actual_line = index_lines[i-1]
        assert actual_line == expected_line, (
            f"merged_index.md line {i} is incorrect. "
            f"Expected '{expected_line.strip()}', got '{actual_line.strip()}'."
        )