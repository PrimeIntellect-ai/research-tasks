# test_final_state.py

import os
import struct
import pytest

def parse_wal(wal_path):
    if not os.path.isfile(wal_path):
        pytest.fail(f"WAL file {wal_path} is missing.")

    with open(wal_path, 'rb') as f:
        data = f.read()

    if not data.startswith(b"BKWAL1\n"):
        pytest.fail("WAL file does not start with BKWAL1\\n")

    pos = 7
    valid_records = []

    while pos < len(data):
        if not data[pos:].startswith(b"BEGIN\n"):
            break
        pos += 6

        # Parse FILE
        nl = data.find(b'\n', pos)
        file_line = data[pos:nl].decode('utf-8')
        pos = nl + 1
        file_path = file_line.split("FILE: ")[1]

        # Parse SIZE
        nl = data.find(b'\n', pos)
        size_line = data[pos:nl].decode('utf-8')
        pos = nl + 1
        size = int(size_line.split("SIZE: ")[1])

        # Parse CHECKSUM
        nl = data.find(b'\n', pos)
        chk_line = data[pos:nl].decode('utf-8')
        pos = nl + 1
        expected_chk = int(chk_line.split("CHECKSUM: ")[1], 16)

        # Parse DATA header
        nl = data.find(b'\n', pos)
        pos = nl + 1

        # Read data
        record_data = data[pos:pos+size]
        pos += size

        # Read END
        nl = data.find(b'\n', pos)
        pos = nl + 1

        # Validate checksum
        actual_chk = sum(record_data) % 256
        if actual_chk == expected_chk:
            valid_records.append({
                "path": file_path,
                "data": record_data
            })

    return valid_records

def test_archive_bin_contents():
    wal_path = "/home/user/backups/db.wal"
    archive_path = "/home/user/backups/archive.bin"

    assert os.path.isfile(archive_path), f"Archive file {archive_path} was not created."

    valid_records = parse_wal(wal_path)

    expected_archive = bytearray()
    for r in valid_records:
        path_bytes = r["path"].encode('utf-8')
        expected_archive.extend(struct.pack('<I', len(path_bytes)))
        expected_archive.extend(path_bytes)
        expected_archive.extend(struct.pack('<I', len(r["data"])))
        expected_archive.extend(r["data"])

    with open(archive_path, 'rb') as f:
        actual_archive = f.read()

    assert actual_archive == expected_archive, f"Contents of {archive_path} do not match the expected binary format."

def test_process_log_contents():
    wal_path = "/home/user/backups/db.wal"
    log_path = "/home/user/backups/process.log"

    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    valid_records = parse_wal(wal_path)

    expected_log_lines = []
    for r in valid_records:
        expected_log_lines.append(f"ARCHIVED {r['path']} {len(r['data'])} bytes\n")

    expected_log = "".join(expected_log_lines)

    with open(log_path, 'r', encoding='utf-8') as f:
        actual_log = f.read()

    assert actual_log == expected_log, f"Contents of {log_path} do not match expected log output."

def test_source_code_uses_fcntl_locks():
    source_path = "/home/user/wal_archiver.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    assert "fcntl" in source_code, "Source code does not contain 'fcntl' for file locking."
    assert "F_WRLCK" in source_code, "Source code does not contain 'F_WRLCK' for exclusive write locking."