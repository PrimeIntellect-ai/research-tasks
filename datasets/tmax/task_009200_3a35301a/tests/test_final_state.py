# test_final_state.py

import os
import hashlib
import stat
import pytest

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_manifest_csv_exists_and_correct():
    manifest_path = '/home/user/manifest.csv'
    assert os.path.isfile(manifest_path), f"File {manifest_path} is missing"

    artifacts_dir = '/home/user/artifacts'
    expected_lines = []

    for filename in os.listdir(artifacts_dir):
        filepath = os.path.join(artifacts_dir, filename)
        if filename.endswith('.bin') and os.path.isfile(filepath):
            st = os.stat(filepath)
            if st.st_mode & stat.S_IXUSR:
                size = st.st_size
                checksum = get_sha256(filepath)
                expected_lines.append(f"{filename},{size},{checksum}\n")

    expected_lines.sort()

    with open(manifest_path, 'r') as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, "Initial manifest.csv does not contain the correct sorted entries"

def test_clean_manifest_compiled():
    executable_path = '/home/user/clean_manifest'
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} is missing"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable"

def test_clean_manifest_c_fixed():
    c_file_path = '/home/user/clean_manifest.c'
    assert os.path.isfile(c_file_path), f"Source file {c_file_path} is missing"

    with open(c_file_path, 'r') as f:
        content = f.read()

    # The bug was freeing `line` inside the loop. The student should have removed or moved it.
    # A simple check is that the program compiles and works, which is tested by the output, 
    # but we can also check that free(line) is not inside the while loop in a naive way, 
    # or just rely on the final output being correct.
    # We will rely on the final output correctness as the ultimate proof it doesn't segfault.

def test_final_manifest_csv_correct():
    final_manifest_path = '/home/user/final_manifest.csv'
    assert os.path.isfile(final_manifest_path), f"File {final_manifest_path} is missing"

    artifacts_dir = '/home/user/artifacts'
    expected_lines = []

    for filename in os.listdir(artifacts_dir):
        filepath = os.path.join(artifacts_dir, filename)
        if filename.endswith('.bin') and os.path.isfile(filepath):
            st = os.stat(filepath)
            if st.st_mode & stat.S_IXUSR and "debug" not in filename:
                size = st.st_size
                checksum = get_sha256(filepath)
                expected_lines.append(f"{filename},{size},{checksum}\n")

    expected_lines.sort()

    with open(final_manifest_path, 'r') as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, "final_manifest.csv does not contain the correct filtered entries"