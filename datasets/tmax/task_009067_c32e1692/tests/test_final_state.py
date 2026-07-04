# test_final_state.py

import os
import pytest

def test_go_file_exists():
    assert os.path.isfile("/home/user/doc_converter.go"), "/home/user/doc_converter.go does not exist"

@pytest.mark.parametrize("expected_path, expected_content", [
    ("intro.md", "# Welcome to the docs"),
    ("api/auth.md", "## Authentication API"),
    ("setup/install.md", "## Installation Instructions"),
    ("api/users/list.md", "## List Users API"),
])
def test_output_markdown_files(expected_path, expected_content):
    full_path = os.path.join("/home/user/docs_out", expected_path)
    assert os.path.isfile(full_path), f"Output file {full_path} was not created"

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content of {full_path} is incorrect"

def test_conversion_log():
    log_path = "/home/user/docs_out/conversion.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created"

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "[SUCCESS] doc1.bin -> intro.md",
        "[SUCCESS] doc2.bin -> api/auth.md",
        "[SUCCESS] doc3.bin -> setup/install.md",
        "[SUCCESS] doc4.bin -> api/users/list.md"
    }

    actual_lines = set(lines)

    assert len(lines) == 4, f"Expected exactly 4 lines in {log_path}, found {len(lines)}"
    assert actual_lines == expected_lines, f"Log file contents do not match expected lines. Missing: {expected_lines - actual_lines}, Unexpected: {actual_lines - expected_lines}"