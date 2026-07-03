# test_final_state.py

import os
import pytest
import glob

def test_text_transformation():
    md_files = [
        "/home/user/docs/intro.md",
        "/home/user/docs/setup.md",
        "/home/user/docs/sub/advanced.md"
    ]
    for md_file in md_files:
        assert os.path.isfile(md_file), f"Markdown file {md_file} is missing."
        with open(md_file, 'r') as f:
            content = f.read()
            assert "DEPRECATED" not in content, f"File {md_file} still contains 'DEPRECATED'."
            assert "OBSOLETE" in content, f"File {md_file} does not contain 'OBSOLETE'."

def test_api_reference_generated():
    api_ref_path = "/home/user/docs/api_reference.md"
    assert os.path.isfile(api_ref_path), f"File {api_ref_path} was not generated."

    with open(api_ref_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_symbols = [
        "ApiDeleteUser",
        "ApiGetUser",
        "ApiUpdateSystem"
    ]

    assert lines == expected_symbols, f"Contents of {api_ref_path} do not match expected symbols or are not sorted."

def test_nav_index_generated():
    nav_index_path = "/home/user/docs/nav_index.txt"
    assert os.path.isfile(nav_index_path), f"File {nav_index_path} was not generated."

    with open(nav_index_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "advanced.md - LastTX: NONE",
        "intro.md - LastTX: 1009",
        "setup.md - LastTX: 1005"
    ]

    assert lines == expected_lines, f"Contents of {nav_index_path} do not match expected navigation index or are not sorted."

def test_go_script_exists():
    script_path = "/home/user/build_nav.go"
    assert os.path.isfile(script_path), f"Go script {script_path} does not exist."