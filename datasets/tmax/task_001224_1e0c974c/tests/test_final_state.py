# test_final_state.py

import os
import struct
import hashlib
import pytest

PROJECT_DIR = '/home/user/project_data'
MANIFEST_V1 = '/home/user/manifest_v1.csv'
MANIFEST_V2 = '/home/user/manifest_v2.csv'
INCREMENTAL_BIN = '/home/user/incremental.bin'

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_current_files_and_hashes():
    files_hashes = {}
    for root, _, files in os.walk(PROJECT_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, PROJECT_DIR)
            files_hashes[rel_path] = compute_sha256(full_path)
    return files_hashes

def get_v1_manifest():
    v1_hashes = {}
    if os.path.exists(MANIFEST_V1):
        with open(MANIFEST_V1, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',', 1)
                    if len(parts) == 2:
                        v1_hashes[parts[0]] = parts[1]
    return v1_hashes

def test_manifest_v2_exists_and_correct():
    """Test that manifest_v2.csv exists and contains exactly the current files and their sha256 hashes."""
    assert os.path.isfile(MANIFEST_V2), f"{MANIFEST_V2} is missing"

    current_files = get_current_files_and_hashes()

    v2_hashes = {}
    with open(MANIFEST_V2, 'r') as f:
        lines = f.read().splitlines()

    for line in lines:
        if not line.strip():
            continue
        parts = line.split(',', 1)
        assert len(parts) == 2, f"Invalid line format in {MANIFEST_V2}: {line}"
        v2_hashes[parts[0]] = parts[1]

    assert set(v2_hashes.keys()) == set(current_files.keys()), "Files in manifest_v2.csv do not match current files in project_data"

    for rel_path, expected_hash in current_files.items():
        assert v2_hashes[rel_path] == expected_hash, f"Hash for {rel_path} in {MANIFEST_V2} is incorrect"

    # Check sorting
    non_empty_lines = [line for line in lines if line.strip()]
    sorted_lines = sorted(non_empty_lines)
    assert non_empty_lines == sorted_lines, f"Lines in {MANIFEST_V2} are not sorted alphabetically"

def test_incremental_bin_exists_and_correct():
    """Test that incremental.bin exists and contains the correct changed files with proper binary format."""
    assert os.path.isfile(INCREMENTAL_BIN), f"{INCREMENTAL_BIN} is missing"

    current_files = get_current_files_and_hashes()
    v1_hashes = get_v1_manifest()

    expected_changed_files = []
    for rel_path, current_hash in current_files.items():
        if rel_path not in v1_hashes or v1_hashes[rel_path] != current_hash:
            expected_changed_files.append(rel_path)

    expected_changed_files.sort()

    with open(INCREMENTAL_BIN, 'rb') as f:
        magic = f.read(4)
        assert magic == b'ARCH', f"Invalid magic header in {INCREMENTAL_BIN}, expected 'ARCH', got {magic}"

        parsed_files = []
        while True:
            path_len_bytes = f.read(4)
            if not path_len_bytes:
                break
            assert len(path_len_bytes) == 4, "Unexpected EOF while reading path_length"
            path_len = struct.unpack('<I', path_len_bytes)[0]

            path_bytes = f.read(path_len)
            assert len(path_bytes) == path_len, "Unexpected EOF while reading path"
            path = path_bytes.decode('utf-8')

            file_size_bytes = f.read(8)
            assert len(file_size_bytes) == 8, "Unexpected EOF while reading file_size"
            file_size = struct.unpack('<Q', file_size_bytes)[0]

            file_data = f.read(file_size)
            assert len(file_data) == file_size, "Unexpected EOF while reading file_data"

            parsed_files.append((path, file_data))

    parsed_paths = [p[0] for p in parsed_files]
    assert parsed_paths == expected_changed_files, f"Expected changed files {expected_changed_files}, but got {parsed_paths} in {INCREMENTAL_BIN}"

    for path, file_data in parsed_files:
        full_path = os.path.join(PROJECT_DIR, path)
        with open(full_path, 'rb') as orig_f:
            expected_data = orig_f.read()
        assert file_data == expected_data, f"File data for {path} in {INCREMENTAL_BIN} does not match actual file content"