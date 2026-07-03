# test_final_state.py

import os
import subprocess
import struct
import hashlib
import pytest

CLEAN_DIR = "/home/user/dataset/clean/"
EVIL_DIR = "/home/user/dataset/evil/"
SANITIZER_BIN = "/home/user/sanitizer"
EXTRACTED_DIR = "/home/user/dataset/extracted/"
MANIFEST_FILE = "/home/user/dataset/manifest.txt"

def parse_darc(filepath):
    """Parses the DARC archive format and returns a list of (path, data) tuples."""
    files = []
    with open(filepath, 'rb') as f:
        data = f.read()

    if not data.startswith(b'DARC'):
        return files

    offset = 4
    if offset + 2 > len(data):
        return files

    file_count = struct.unpack_from('<H', data, offset)[0]
    offset += 2

    for _ in range(file_count):
        if offset + 2 > len(data):
            break
        path_len = struct.unpack_from('<H', data, offset)[0]
        offset += 2

        if offset + path_len > len(data):
            break
        path = data[offset:offset+path_len].decode('utf-8', errors='replace')
        offset += path_len

        if offset + 4 > len(data):
            break
        file_size = struct.unpack_from('<I', data, offset)[0]
        offset += 4

        if offset + file_size > len(data):
            break
        file_data = data[offset:offset+file_size]
        offset += file_size

        files.append((path, file_data))

    return files

def test_sanitizer_exists():
    assert os.path.exists(SANITIZER_BIN), f"Sanitizer binary not found at {SANITIZER_BIN}"
    assert os.path.isfile(SANITIZER_BIN), f"{SANITIZER_BIN} is not a file"
    assert os.access(SANITIZER_BIN, os.X_OK), f"Sanitizer binary at {SANITIZER_BIN} is not executable"

def test_sanitizer_on_corpora():
    evil_bypassed = []
    clean_rejected = []

    # Test evil corpus
    if os.path.exists(EVIL_DIR):
        for filename in os.listdir(EVIL_DIR):
            filepath = os.path.join(EVIL_DIR, filename)
            if not os.path.isfile(filepath):
                continue
            result = subprocess.run([SANITIZER_BIN, filepath], capture_output=True)
            if result.returncode != 1:
                evil_bypassed.append(filename)

    # Test clean corpus
    if os.path.exists(CLEAN_DIR):
        for filename in os.listdir(CLEAN_DIR):
            filepath = os.path.join(CLEAN_DIR, filename)
            if not os.path.isfile(filepath):
                continue
            result = subprocess.run([SANITIZER_BIN, filepath], capture_output=True)
            if result.returncode != 0:
                clean_rejected.append(filename)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} evil archives bypassed sanitizer (expected exit code 1): {evil_bypassed[:5]}")
    if clean_rejected:
        error_msg.append(f"{len(clean_rejected)} clean archives rejected by sanitizer (expected exit code 0): {clean_rejected[:5]}")

    assert not evil_bypassed and not clean_rejected, " | ".join(error_msg)

def test_extracted_files_and_manifest():
    assert os.path.exists(EXTRACTED_DIR), f"Extracted directory not found at {EXTRACTED_DIR}"
    assert os.path.isdir(EXTRACTED_DIR), f"{EXTRACTED_DIR} is not a directory"
    assert os.path.exists(MANIFEST_FILE), f"Manifest file not found at {MANIFEST_FILE}"

    expected_files = {}
    expected_manifest_lines = set()

    for filename in os.listdir(CLEAN_DIR):
        filepath = os.path.join(CLEAN_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        parsed_files = parse_darc(filepath)
        for path, data in parsed_files:
            file_hash = hashlib.sha256(data).hexdigest()
            expected_files[f"{file_hash}.log"] = data
            expected_manifest_lines.add(f"{file_hash} {path}")

    # Verify extracted files
    actual_files = set(os.listdir(EXTRACTED_DIR))
    expected_filenames = set(expected_files.keys())

    missing_files = expected_filenames - actual_files
    extra_files = actual_files - expected_filenames

    assert not missing_files, f"Missing extracted files: {list(missing_files)[:5]}"
    assert not extra_files, f"Extra files found in extracted directory: {list(extra_files)[:5]}"

    for filename, expected_data in expected_files.items():
        filepath = os.path.join(EXTRACTED_DIR, filename)
        with open(filepath, 'rb') as f:
            actual_data = f.read()
        assert actual_data == expected_data, f"Data mismatch in extracted file: {filename}"

    # Verify manifest
    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        actual_manifest_lines = set(line.strip() for line in f if line.strip())

    missing_manifest = expected_manifest_lines - actual_manifest_lines
    extra_manifest = actual_manifest_lines - expected_manifest_lines

    assert not missing_manifest, f"Missing entries in manifest: {list(missing_manifest)[:5]}"
    assert not extra_manifest, f"Extra entries in manifest: {list(extra_manifest)[:5]}"