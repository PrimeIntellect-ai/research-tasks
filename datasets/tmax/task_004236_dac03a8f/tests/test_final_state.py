# test_final_state.py

import os
import pytest

FINAL_DOCS_DIR = "/home/user/final_docs"
EXTRACTED_DOCS_DIR = "/home/user/extracted_docs"

def test_directories_exist():
    assert os.path.isdir(EXTRACTED_DOCS_DIR), f"Directory {EXTRACTED_DOCS_DIR} does not exist."
    assert os.path.isdir(FINAL_DOCS_DIR), f"Directory {FINAL_DOCS_DIR} does not exist."

def test_extracted_docs_contents():
    extracted_files = set(os.listdir(EXTRACTED_DOCS_DIR))
    expected_files = {'intro.txt', 'report.txt', 'normal.txt'}

    assert extracted_files == expected_files, f"Extracted files mismatch. Found: {extracted_files}, Expected: {expected_files}"

def test_final_docs_contents():
    final_files = set(os.listdir(FINAL_DOCS_DIR))
    expected_files = {'intro.txt', 'report.txt', 'normal.txt'}

    assert final_files == expected_files, f"Final files mismatch. Found: {final_files}, Expected: {expected_files}"

def test_final_docs_text_transformations():
    expected_contents = {
        'intro.txt': (
            "Welcome to Acme Corp!\n"
            "We are excited to have you. Acme Corp values its employees.\n"
            "End of document."
        ),
        'report.txt': (
            "The Acme Corp quarterly report.\n"
            "Revenue is up by 15% at Acme Corp."
        ),
        'normal.txt': (
            "Just a normal file.\n"
            "No drafts here.\n"
            "Only Acme Corp everywhere."
        )
    }

    for filename, expected_text in expected_contents.items():
        filepath = os.path.join(FINAL_DOCS_DIR, filename)
        assert os.path.isfile(filepath), f"File {filepath} is missing."

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        assert content == expected_text, f"Content of {filepath} does not match expected transformations.\nExpected:\n{expected_text}\n\nGot:\n{content}"