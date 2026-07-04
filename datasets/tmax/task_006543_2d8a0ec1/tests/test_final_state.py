# test_final_state.py

import os
import pytest

def test_zip_slip_log():
    log_path = '/home/user/zip_slip.log'
    assert os.path.exists(log_path), f"{log_path} does not exist. Zip Slip mitigation log is missing."
    with open(log_path, 'r') as f:
        content = f.read().strip()
    assert content == '../../../home/user/malicious.sh', f"Expected log to contain skipped malicious path, got: {content}"

def test_restored_wal_file():
    wal_path = '/home/user/restored/valid_log.wal'
    assert os.path.exists(wal_path), f"{wal_path} does not exist. WAL file was not extracted."
    with open(wal_path, 'rb') as f:
        content = f.read()
    expected = b'WAL\x00 + some random WAL data for testing'
    assert content == expected, f"Content of {wal_path} is incorrect."

def test_restored_elf_file():
    elf_path = '/home/user/restored/bin/system_tool'
    assert os.path.exists(elf_path), f"{elf_path} does not exist. ELF file was not extracted."
    with open(elf_path, 'rb') as f:
        content = f.read()
    expected = b'\x7fELF + valid binary data here'
    assert content == expected, f"Content of {elf_path} is incorrect."

def test_ignored_files():
    notes_path = '/home/user/restored/random_notes.txt'
    assert not os.path.exists(notes_path), f"{notes_path} should not have been extracted because of invalid magic bytes."

def test_malicious_file_not_extracted():
    malicious_path = '/home/user/malicious.sh'
    assert not os.path.exists(malicious_path), f"{malicious_path} exists! Path traversal vulnerability was not prevented."