# test_final_state.py

import os
import pytest

def test_valid_files_txt():
    valid_files_path = "/home/user/valid_files.txt"
    assert os.path.isfile(valid_files_path), f"Missing {valid_files_path}"

    with open(valid_files_path, 'r') as f:
        content = f.read().splitlines()

    # doc_a1.md, doc_c3.md, and doc_d4.md are > 50 bytes
    assert "doc_a1.md" in content, "doc_a1.md should be in valid_files.txt"
    assert "doc_c3.md" in content, "doc_c3.md should be in valid_files.txt"
    assert "doc_d4.md" in content, "doc_d4.md should be in valid_files.txt"
    assert "doc_b2.md" not in content, "doc_b2.md should NOT be in valid_files.txt (<= 50 bytes)"

def test_organized_docs_structure():
    eng_file = "/home/user/organized_docs/Engineering/API_V2_Specs_r4.md"
    mkt_file = "/home/user/organized_docs/Marketing/Brand_Guide_r2.md"
    hr_file = "/home/user/organized_docs/HR/Leave_Policy_r1.md"

    assert os.path.isfile(eng_file), f"Missing {eng_file}"
    assert os.path.isfile(mkt_file), f"Missing {mkt_file}"
    assert not os.path.exists(hr_file), f"File {hr_file} should not exist (doc_b2.md was <= 50 bytes)"

    with open(eng_file, 'r') as f:
        eng_content = f.read()
    assert "This is a valid engineering document" in eng_content, "Incorrect content in Engineering doc"

    with open(mkt_file, 'r') as f:
        mkt_content = f.read()
    assert "Marketing guidelines for Q3" in mkt_content, "Incorrect content in Marketing doc"

def test_final_inventory():
    inventory_path = "/home/user/final_inventory.txt"
    assert os.path.isfile(inventory_path), f"Missing {inventory_path}"

    with open(inventory_path, 'r') as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    expected_lines = [
        "Engineering/API_V2_Specs_r4.md",
        "Marketing/Brand_Guide_r2.md"
    ]

    assert lines == expected_lines, f"Expected {inventory_path} to contain exactly {expected_lines}, but got {lines}"

def test_c_program_exists():
    c_source = "/home/user/organizer.c"
    c_bin = "/home/user/organizer"

    assert os.path.isfile(c_source), f"Missing C source file {c_source}"
    assert os.path.isfile(c_bin), f"Missing compiled binary {c_bin}"
    assert os.access(c_bin, os.X_OK), f"Binary {c_bin} is not executable"