# test_final_state.py

import os
import pytest

def test_setup_md_updated():
    setup_md_path = "/home/user/docs/setup.md"
    assert os.path.isfile(setup_md_path), f"File {setup_md_path} is missing"

    with open(setup_md_path, "r") as f:
        content = f.read()

    expected_json = '{\n  "author": "alice",\n  "status": "review"\n}'
    original_content = '# Setup Guide\nThis is the setup guide.\n'

    assert expected_json in content, f"Expected JSON not found in {setup_md_path}"
    assert original_content.strip() in content, f"Original content missing in {setup_md_path}"
    assert content.startswith(expected_json), f"{setup_md_path} does not start with the expected JSON block"
    assert "\n\n# Setup Guide" in content or "\n\n\n# Setup Guide" in content, "Missing blank line before original content"

def test_api_md_updated():
    api_md_path = "/home/user/docs/api.md"
    assert os.path.isfile(api_md_path), f"File {api_md_path} is missing"

    with open(api_md_path, "r") as f:
        content = f.read()

    expected_json = '{\n  "author": "bob",\n  "status": "published"\n}'
    original_content = '# API Reference\nList of endpoints.\n'

    assert expected_json in content, f"Expected JSON not found in {api_md_path}"
    assert original_content.strip() in content, f"Original content missing in {api_md_path}"
    assert content.startswith(expected_json), f"{api_md_path} does not start with the expected JSON block"
    assert "\n\n# API Reference" in content or "\n\n\n# API Reference" in content, "Missing blank line before original content"

def test_csv_registry():
    csv_file_path = "/home/user/docs/updated_registry.csv"
    assert os.path.isfile(csv_file_path), f"File {csv_file_path} is missing"

    with open(csv_file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_line_1 = "/home/user/docs/setup.md,alice,review"
    expected_line_2 = "/home/user/docs/api.md,bob,published"

    assert expected_line_1 in lines, f"Expected line '{expected_line_1}' not found in CSV"
    assert expected_line_2 in lines, f"Expected line '{expected_line_2}' not found in CSV"

def test_go_script_exists_and_uses_flock():
    go_script_path = "/home/user/fix_docs.go"
    assert os.path.isfile(go_script_path), f"Go script {go_script_path} is missing"

    with open(go_script_path, "r") as f:
        content = f.read()

    assert "syscall.Flock" in content, "Go script does not contain 'syscall.Flock'"
    assert "syscall.LOCK_EX" in content, "Go script does not contain 'syscall.LOCK_EX'"