# test_final_state.py

import os
import pytest

def test_script_exists_and_atomic_write():
    script_path = '/home/user/build_docs.py'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    with open(script_path, 'r', encoding='utf-8') as f:
        script_content = f.read()

    # Check for atomic write logic
    has_atomic = any(func in script_content for func in ['os.replace', 'os.rename', 'shutil.move'])
    assert has_atomic, "Atomic write logic (os.replace, os.rename, or shutil.move) is missing in the script."

def test_final_doc_content():
    doc_path = '/home/user/final_doc.md'
    assert os.path.exists(doc_path), f"The final document {doc_path} does not exist."
    assert os.path.isfile(doc_path), f"{doc_path} is not a file."

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "# API Documentation" in content, "final_doc.md is missing API Documentation."
    assert "# Introduction" in content, "final_doc.md is missing Introduction."
    assert "# Setup Instructions" in content, "final_doc.md is missing Setup Instructions."

    # Check alphabetical order
    idx_api = content.find("# API")
    idx_intro = content.find("# Introduction")
    idx_setup = content.find("# Setup")

    assert idx_api < idx_intro < idx_setup, "The contents are not concatenated in alphabetical order of their filenames."

def test_char_count_file():
    count_path = '/home/user/char_count.txt'
    doc_path = '/home/user/final_doc.md'

    assert os.path.exists(count_path), f"The character count file {count_path} does not exist."
    assert os.path.isfile(count_path), f"{count_path} is not a file."
    assert os.path.exists(doc_path), f"Cannot verify char count because {doc_path} is missing."

    with open(doc_path, 'r', encoding='utf-8') as f:
        actual_content_len = len(f.read())

    with open(count_path, 'r', encoding='utf-8') as f:
        count_str = f.read().strip()

    assert count_str.isdigit(), "The content of char_count.txt is not a valid integer."
    assert int(count_str) == actual_content_len, f"Expected character count {actual_content_len}, but got {count_str} in char_count.txt."