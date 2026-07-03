# test_final_state.py

import os
import hashlib
import tarfile
import re
import io
import tempfile
import pytest

DATA_DIR = "/home/user/data"
BACKUP_OUT_DIR = "/home/user/backup_out"
BASELINE_FILE = "/home/user/baseline.txt"
NEW_BASELINE_FILE = "/home/user/new_baseline.txt"
ATOMIC_LOG_FILE = "/home/user/atomic_ops.log"

FILE1 = os.path.join(DATA_DIR, "file1.txt")
FILE2 = os.path.join(DATA_DIR, "file2.txt")
FILE3 = os.path.join(DATA_DIR, "file3.txt")

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_backup_parts_exist_and_sizes():
    assert os.path.isdir(BACKUP_OUT_DIR), f"Backup directory missing: {BACKUP_OUT_DIR}"
    files = sorted(os.listdir(BACKUP_OUT_DIR))
    bck_files = [f for f in files if re.match(r"^part-\d{3}\.bck$", f)]
    assert len(bck_files) > 0, "No part-XXX.bck files found in backup directory."

    # Check that there are no tmp files left
    tmp_files = [f for f in files if f.endswith(".tmp")]
    assert len(tmp_files) == 0, f"Temporary files found in backup directory: {tmp_files}"

    # Check sizes
    for i, bck_file in enumerate(bck_files):
        filepath = os.path.join(BACKUP_OUT_DIR, bck_file)
        size = os.path.getsize(filepath)
        if i < len(bck_files) - 1:
            assert size == 51200, f"Chunk {bck_file} is {size} bytes, expected exactly 51200 bytes."
        else:
            assert size <= 51200, f"Last chunk {bck_file} is {size} bytes, expected <= 51200 bytes."

def test_archive_concatenation_and_contents():
    bck_files = sorted([f for f in os.listdir(BACKUP_OUT_DIR) if re.match(r"^part-\d{3}\.bck$", f)])
    assert len(bck_files) > 0, "No part-XXX.bck files found."

    concatenated_data = bytearray()
    for bck_file in bck_files:
        with open(os.path.join(BACKUP_OUT_DIR, bck_file), "rb") as f:
            concatenated_data.extend(f.read())

    # Write concatenated data to a temporary file to read with tarfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(concatenated_data)
        tmp_path = tmp.name

    try:
        assert tarfile.is_tarfile(tmp_path), "Concatenated chunks do not form a valid tar archive."

        with tarfile.open(tmp_path, "r:gz") as tar:
            members = tar.getnames()
            # The archive should contain file2.txt and file3.txt, but NOT file1.txt
            # Allow paths like 'file2.txt' or './file2.txt' or 'data/file2.txt' depending on how tar was created,
            # but the requirement says "preserve their relative paths from within /home/user/data/"
            # So they should be 'file2.txt' and 'file3.txt'

            basenames = [os.path.basename(m) for m in members]
            assert "file1.txt" not in basenames, "file1.txt should not be in the archive."
            assert "file2.txt" in basenames, "file2.txt missing from the archive."
            assert "file3.txt" in basenames, "file3.txt missing from the archive."

            # Check contents of extracted files match original
            for member in tar.getmembers():
                if member.isfile():
                    extracted_f = tar.extractfile(member)
                    extracted_content = extracted_f.read()
                    original_path = os.path.join(DATA_DIR, os.path.basename(member.name))
                    with open(original_path, "rb") as orig_f:
                        original_content = orig_f.read()
                    assert extracted_content == original_content, f"Content of {member.name} in archive does not match original."
    finally:
        os.remove(tmp_path)

def test_atomic_ops_log():
    assert os.path.isfile(ATOMIC_LOG_FILE), f"Atomic ops log missing: {ATOMIC_LOG_FILE}"

    with open(ATOMIC_LOG_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    bck_files = sorted([f for f in os.listdir(BACKUP_OUT_DIR) if re.match(r"^part-\d{3}\.bck$", f)])
    assert len(lines) >= len(bck_files), "Not enough log entries in atomic_ops.log"

    for i, bck_file in enumerate(bck_files):
        expected_line = f"Renamed part-{i:03d}.tmp to part-{i:03d}.bck"
        assert any(expected_line in line for line in lines), f"Expected log entry '{expected_line}' not found."

def test_new_baseline():
    assert os.path.isfile(NEW_BASELINE_FILE), f"New baseline file missing: {NEW_BASELINE_FILE}"

    with open(NEW_BASELINE_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected exactly 3 lines in {NEW_BASELINE_FILE}"

    entries = {}
    for line in lines:
        parts = line.split()
        assert len(parts) == 2, f"Invalid format in new_baseline.txt line: {line}"
        entries[parts[1]] = parts[0]

    actual_hash1 = get_sha256(FILE1)
    actual_hash2 = get_sha256(FILE2)
    actual_hash3 = get_sha256(FILE3)

    assert "file1.txt" in entries, "file1.txt missing from new baseline"
    assert "file2.txt" in entries, "file2.txt missing from new baseline"
    assert "file3.txt" in entries, "file3.txt missing from new baseline"

    assert entries["file1.txt"] == actual_hash1, "Hash for file1.txt is incorrect in new baseline"
    assert entries["file2.txt"] == actual_hash2, "Hash for file2.txt is incorrect in new baseline"
    assert entries["file3.txt"] == actual_hash3, "Hash for file3.txt is incorrect in new baseline"