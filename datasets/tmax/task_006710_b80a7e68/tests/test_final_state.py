# test_final_state.py

import os
import hashlib
import stat
import pytest

def test_c_source_exists():
    c_file = "/home/user/doc_indexer.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."

def test_executable_exists():
    exe_file = "/home/user/doc_indexer"
    assert os.path.isfile(exe_file), f"Executable file {exe_file} is missing."

    # Check if the file is executable
    st = os.stat(exe_file)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File {exe_file} is not executable."

def test_manifest_content():
    manifest_file = "/home/user/doc_manifest.txt"
    assert os.path.isfile(manifest_file), f"Manifest file {manifest_file} is missing."

    base_dir = "/home/user/docs_repo"
    expected_entries = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".draft"):
                continue
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, base_dir)

            with open(filepath, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            expected_entries.append((file_hash, f"./{relpath}"))

    # Sort by hash (first column) to match the required output
    expected_entries.sort(key=lambda x: x[0])

    with open(manifest_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    actual_entries = []
    for line in actual_lines:
        parts = line.split()
        assert len(parts) >= 2, f"Invalid line format in manifest: '{line}'"
        actual_entries.append((parts[0], parts[1]))

    assert len(actual_entries) == len(expected_entries), f"Expected {len(expected_entries)} entries in manifest, found {len(actual_entries)}."

    for i, (expected_hash, expected_path) in enumerate(expected_entries):
        actual_hash, actual_path = actual_entries[i]
        assert actual_hash == expected_hash, f"Line {i+1}: Expected hash {expected_hash} for {expected_path}, got {actual_hash}."
        assert actual_path == expected_path, f"Line {i+1}: Expected path {expected_path}, got {actual_path}."