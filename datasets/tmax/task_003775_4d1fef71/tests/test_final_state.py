# test_final_state.py
import os
import struct
import pytest

ARCHIVE_PATH = "/home/user/archive.bin"
LOG_PATH = "/home/user/logs/config_updates.log"

def test_archive_exists():
    """Test that the archive file has been created."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist. Did the backup_tool run?"

def test_archive_size_threshold():
    """Test that the archive file size is strictly less than 250,000 bytes."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist."
    size = os.path.getsize(ARCHIVE_PATH)
    assert size < 250000, f"Archive size {size} bytes exceeds the threshold of 250,000 bytes."
    assert size > 10, f"Archive size {size} bytes is too small to contain actual backup data."

def test_archive_header():
    """Test that the archive file has the exact required 10-byte header."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist."
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} does not exist."

    # Derive the expected number of committed files from the log
    with open(LOG_PATH, "r") as f:
        content = f.read()

    expected_count = content.count("STATE: COMMITTED")
    assert expected_count > 0, "No committed states found in the log file."

    with open(ARCHIVE_PATH, "rb") as f:
        header = f.read(10)

    assert len(header) == 10, f"Archive file header is too short: {len(header)} bytes."

    magic, version, count = struct.unpack('<4sHI', header)

    assert magic == b'BCKP', f"Invalid magic bytes: expected b'BCKP', got {magic}"
    assert version == 1, f"Invalid version: expected 1, got {version}"
    assert count == expected_count, f"Invalid entry count: expected {expected_count}, got {count}"