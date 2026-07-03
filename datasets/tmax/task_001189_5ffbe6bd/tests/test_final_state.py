# test_final_state.py

import os
import pytest

def test_cleaner_go_exists_and_uses_atomic_writes():
    """Verify that cleaner.go exists and appears to use atomic writes."""
    go_file = "/home/user/cleaner.go"
    assert os.path.isfile(go_file), f"Go source file {go_file} does not exist."

    with open(go_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "os.Rename" in content or "Rename" in content, "The Go program does not appear to use os.Rename for atomic writes."
    assert "Temp" in content or ".tmp" in content, "The Go program does not appear to use temporary files for atomic writes."

def test_clean_data_structure_and_content():
    """Verify that the clean_data directory has the correct mirrored structure and UTF-8 files."""
    expected_files = {
        "/home/user/clean_data/alpha/log1.txt": "Temperature: 25°C".encode("utf-8"),
        "/home/user/clean_data/alpha/log2.txt": "Status: OK ✓".encode("utf-8"),
        "/home/user/clean_data/beta/nested/log3.txt": "Warning: \nLow battery".encode("utf-8")
    }

    for filepath, expected_bytes in expected_files.items():
        assert os.path.isfile(filepath), f"Expected converted file {filepath} does not exist."
        with open(filepath, "rb") as f:
            content = f.read()
        assert content == expected_bytes, f"Content of {filepath} does not match expected UTF-8 bytes. Expected {expected_bytes}, got {content}."

def test_tmp_directory_exists():
    """Verify that the .tmp directory exists as required for atomic writes."""
    tmp_dir = "/home/user/clean_data/.tmp"
    assert os.path.isdir(tmp_dir), f"Temporary directory {tmp_dir} does not exist."

def test_summary_file():
    """Verify that summary.txt exists and contains the correct counts."""
    summary_file = "/home/user/summary.txt"
    assert os.path.isfile(summary_file), f"Summary file {summary_file} does not exist."

    with open(summary_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Summary file should contain exactly 2 lines, found {len(lines)}."
    assert lines[0] == "3", f"Expected first line to be '3' (total files), got '{lines[0]}'."
    assert lines[1] == "53", f"Expected second line to be '53' (total bytes), got '{lines[1]}'."