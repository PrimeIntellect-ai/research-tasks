# test_final_state.py

import os
import hashlib
import pytest

RESTORE_DIR = '/home/user/restore'
FINAL_HASHES_FILE = '/home/user/final_hashes.txt'
MERGED_TAR = '/home/user/merged.tar.gz'

def test_merged_tarball_exists():
    assert os.path.isfile(MERGED_TAR), f"{MERGED_TAR} was not created."
    assert os.path.getsize(MERGED_TAR) > 0, f"{MERGED_TAR} is empty."

def test_file3_deleted():
    file3_path = os.path.join(RESTORE_DIR, 'file3.txt')
    assert not os.path.exists(file3_path), f"file3.txt should have been deleted from {RESTORE_DIR}."

def test_file1_content():
    file1_path = os.path.join(RESTORE_DIR, 'file1.txt')
    assert os.path.isfile(file1_path), f"{file1_path} is missing."

    expected_content = b"Base data AAppended data A"
    with open(file1_path, 'rb') as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"Content of {file1_path} is incorrect. Expected {expected_content}, got {actual_content}."

def test_file2_content():
    file2_path = os.path.join(RESTORE_DIR, 'file2.bin')
    assert os.path.isfile(file2_path), f"{file2_path} is missing."

    expected_content = (b'\x01' * 100) + (b'\x02' * 50)
    with open(file2_path, 'rb') as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"Content of {file2_path} is incorrect."

def test_final_hashes_file():
    assert os.path.isfile(FINAL_HASHES_FILE), f"{FINAL_HASHES_FILE} was not created."

    # Compute expected hashes
    f1_content = b"Base data AAppended data A"
    f1_hash = hashlib.sha256(f1_content).hexdigest()

    f2_content = (b'\x01' * 100) + (b'\x02' * 50)
    f2_hash = hashlib.sha256(f2_content).hexdigest()

    with open(FINAL_HASHES_FILE, 'r') as f:
        lines = f.read().strip().split('\n')

    # Parse lines to a dict
    actual_hashes = {}
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2:
            h, p = parts[0], parts[1]
            actual_hashes[p] = h

    assert './file1.txt' in actual_hashes, "./file1.txt missing from final_hashes.txt"
    assert actual_hashes['./file1.txt'] == f1_hash, f"Hash for ./file1.txt is incorrect in {FINAL_HASHES_FILE}"

    assert './file2.bin' in actual_hashes, "./file2.bin missing from final_hashes.txt"
    assert actual_hashes['./file2.bin'] == f2_hash, f"Hash for ./file2.bin is incorrect in {FINAL_HASHES_FILE}"

    assert './file3.txt' not in actual_hashes, "./file3.txt should not be present in final_hashes.txt"

def test_no_extra_files_in_restore():
    expected_files = {'file1.txt', 'file2.bin'}
    actual_files = set(os.listdir(RESTORE_DIR))
    assert actual_files == expected_files, f"Unexpected files in {RESTORE_DIR}: {actual_files - expected_files}"