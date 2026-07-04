# test_final_state.py

import os
import pytest

def test_clean_docs_intro():
    path = "/home/user/clean_docs/docs/intro.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "GlobalTech" in content, f"'GlobalTech' not found in {path}."
    assert "AcmeCorp" not in content, f"'AcmeCorp' still found in {path}."
    assert "Welcome to the GlobalTech documentation." in content
    assert "GlobalTech provides the best widgets." in content

def test_clean_docs_finance():
    path = "/home/user/clean_docs/docs/manuals/finance.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "GlobalTech" in content, f"'GlobalTech' not found in {path}."
    assert "AcmeCorp" not in content, f"'AcmeCorp' still found in {path}."
    assert "GlobalTech financial report for the café." in content

def test_clean_docs_api():
    path = "/home/user/clean_docs/docs/api/index.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "GlobalTech" in content, f"'GlobalTech' not found in {path}."
    assert "AcmeCorp" not in content, f"'AcmeCorp' still found in {path}."
    assert "GlobalTech API résumé." in content

def test_symlink_skipped():
    path = "/home/user/clean_docs/docs/manuals/loop_back"
    assert not os.path.exists(path), f"Symlink directory {path} should have been skipped and not copied."
    assert not os.path.islink(path), f"Symlink {path} should not exist."

def test_migration_log():
    path = "/home/user/migration.log"
    assert os.path.exists(path), f"Log file {path} does not exist."
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in {path}, got {len(lines)}."

    # Check sorting
    assert lines == sorted(lines), "Log file lines are not sorted alphabetically."

    # Check specific lines
    # api/index.txt
    assert "docs/api/index.txt" in lines[0]
    assert any(enc in lines[0].lower() for enc in ["iso-8859-1", "iso8859-1", "latin-1", "latin1", "windows-1252"]), f"Incorrect encoding for index.txt in log: {lines[0]}"

    # intro.txt
    assert "docs/intro.txt" in lines[1]
    assert "utf-8" in lines[1].lower() or "utf8" in lines[1].lower(), f"Incorrect encoding for intro.txt in log: {lines[1]}"

    # manuals/finance.txt
    assert "docs/manuals/finance.txt" in lines[2]
    assert any(enc in lines[2].lower() for enc in ["iso-8859-1", "iso8859-1", "latin-1", "latin1", "windows-1252"]), f"Incorrect encoding for finance.txt in log: {lines[2]}"