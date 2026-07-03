# test_final_state.py
import os
import pytest

def test_merged_bin_correct():
    merged_path = "/home/user/merged.bin"
    assert os.path.isfile(merged_path), f"{merged_path} does not exist."

    fragments = [
        "/home/user/backup_drive/folder2/chunk_A.frag",
        "/home/user/backup_drive/folder1/subfolder/chunk_B.frag",
        "/home/user/backup_drive/chunk_C.frag"
    ]

    expected_bytes = b""
    for frag in fragments:
        if os.path.isfile(frag):
            with open(frag, "rb") as f:
                expected_bytes += f.read()

    with open(merged_path, "rb") as f:
        actual_bytes = f.read()

    assert actual_bytes == expected_bytes, "The contents of merged.bin do not match the expected concatenated fragments in alphabetical order."

def test_parser_c_exists():
    parser_path = "/home/user/parser.c"
    assert os.path.isfile(parser_path), f"{parser_path} does not exist."

def test_critical_logs_correct():
    logs_path = "/home/user/critical_logs.txt"
    assert os.path.isfile(logs_path), f"{logs_path} does not exist."

    with open(logs_path, "r") as f:
        content = f.read()

    parts = [p.strip() for p in content.split("---")]
    parts = [p for p in parts if p]

    expected_1 = "Log Entry 2\nStatus: CRITICAL\nDatabase connection lost.\nRetrying..."
    expected_2 = "Log Entry 4\nStatus: CRITICAL\nDisk failure detected on /dev/sda1.\nImmediate action required."

    assert len(parts) == 2, f"Expected exactly 2 CRITICAL log entries separated by '---', found {len(parts)}."

    # Check that both expected entries are present in the parsed parts
    found_1 = any(expected_1 in p for p in parts)
    found_2 = any(expected_2 in p for p in parts)

    assert found_1, "The first expected CRITICAL log entry (Log Entry 2) was not found or is incomplete."
    assert found_2, "The second expected CRITICAL log entry (Log Entry 4) was not found or is incomplete."