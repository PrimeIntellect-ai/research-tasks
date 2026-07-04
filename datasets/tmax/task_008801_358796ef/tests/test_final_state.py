# test_final_state.py

import os
import zlib
import struct
import pytest

ARCHIVE_PATH = "/home/user/backup_dir/final_backup.carc"
LOG_PATH = "/home/user/backup_operation.log"

def test_archive_exists():
    """Verify that the final backup archive exists."""
    assert os.path.isdir("/home/user/backup_dir"), "Backup directory /home/user/backup_dir/ does not exist."
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist."

def test_log_file_exists_and_content():
    """Verify that the log file exists and contains the atomic rename confirmation."""
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} does not exist."

    with open(LOG_PATH, 'r') as f:
        log_content = f.read()

    assert "Atomically renamed" in log_content, "Log file missing 'Atomically renamed' confirmation."
    assert "final_backup.carc" in log_content, "Log file missing the final backup file name."

def test_archive_structure_and_content():
    """Verify the archive header, structure, and decompression logic."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist."

    with open(ARCHIVE_PATH, 'rb') as f:
        header = f.read(8)
        assert header == b'CUST_ARC', f"Invalid header: expected b'CUST_ARC', got {header!r}"

        extracted = {}
        while True:
            path_len_data = f.read(2)
            if not path_len_data:
                break

            assert len(path_len_data) == 2, "Unexpected EOF while reading path length."
            path_len = struct.unpack('<H', path_len_data)[0]

            rel_path_data = f.read(path_len)
            assert len(rel_path_data) == path_len, "Unexpected EOF while reading relative path."
            rel_path = rel_path_data.decode('utf-8')

            size_data = f.read(4)
            assert len(size_data) == 4, "Unexpected EOF while reading compressed size."
            comp_size = struct.unpack('<I', size_data)[0]

            comp_payload = f.read(comp_size)
            assert len(comp_payload) == comp_size, "Unexpected EOF while reading payload."

            try:
                reversed_bytes = zlib.decompress(comp_payload)
                original_bytes = reversed_bytes[::-1]
                extracted[rel_path] = original_bytes
            except Exception as e:
                pytest.fail(f"Failed decompression for {rel_path}: {e}")

    expected_files = {
        "app/error.log": b"Error: DB connection timeout\n",
        "app/sys.log": b"System started at 00:00\n",
        "db/query.log": b"SELECT * FROM users;\n",
        "readme.txt": b"Read me first!\n"
    }

    # Verify that excluded files are not in the archive
    assert "app/config.json" not in extracted, "Archive incorrectly contains excluded file app/config.json"

    # Verify expected files are present and match expected content
    for rel_path, expected_content in expected_files.items():
        assert rel_path in extracted, f"Missing file in archive: {rel_path}"
        assert extracted[rel_path] == expected_content, f"Content mismatch for {rel_path}. Expected {expected_content!r}, got {extracted[rel_path]!r}"

    # Verify the order of entries in the archive matches alphabetical order
    extracted_paths = list(extracted.keys())
    assert extracted_paths == sorted(extracted_paths), "Files in the archive are not sorted alphabetically by relative path."