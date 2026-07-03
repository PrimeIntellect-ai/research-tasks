# test_final_state.py

import os
import struct
import pytest

def test_tracker_files_exist():
    """Check that the C source and executable exist."""
    assert os.path.isfile("/home/user/tracker.c"), "/home/user/tracker.c does not exist."
    assert os.path.isfile("/home/user/tracker"), "/home/user/tracker does not exist."
    assert os.access("/home/user/tracker", os.X_OK), "/home/user/tracker is not executable."

def test_configs_directory_exists():
    """Check that the configs directory exists."""
    assert os.path.isdir("/home/user/configs"), "/home/user/configs directory does not exist."

def test_journal_dump_exists():
    """Check that the hex dump was generated."""
    assert os.path.isfile("/home/user/journal_dump.txt"), "/home/user/journal_dump.txt does not exist."

def test_config_journal_binary():
    """Check the size and contents of the binary journal file."""
    journal_path = "/home/user/config_journal.bin"
    assert os.path.isfile(journal_path), f"{journal_path} does not exist."

    file_size = os.path.getsize(journal_path)
    assert file_size == 584, f"Expected journal file size to be 584 bytes, but got {file_size} bytes."

    with open(journal_path, "rb") as f:
        data = f.read()

    assert len(data) == 584, "Read length does not match expected 584 bytes."

    record1 = data[0:292]
    record2 = data[292:584]

    def parse_record(record_bytes):
        filename_bytes, length, content_bytes = struct.unpack("<32sI256s", record_bytes)
        filename = filename_bytes.rstrip(b'\x00').decode('utf-8', errors='replace')
        return filename, length, content_bytes

    parsed_records = {
        parse_record(record1)[0]: parse_record(record1),
        parse_record(record2)[0]: parse_record(record2),
    }

    assert "app.conf" in parsed_records, "Record for app.conf not found in journal."
    assert "user.conf" in parsed_records, "Record for user.conf not found in journal."

    # Check app.conf
    app_filename, app_length, app_content = parsed_records["app.conf"]
    assert app_length == 6, f"Expected length 6 for app.conf, got {app_length}"
    expected_app_content = b"Caf\xc3\xa9\n"
    assert app_content.startswith(expected_app_content), "Content for app.conf does not match expected UTF-8."

    # Check user.conf
    user_filename, user_length, user_content = parsed_records["user.conf"]
    assert user_length == 6, f"Expected length 6 for user.conf, got {user_length}"
    expected_user_content = b"Ni\xc3\xb1o\n"
    assert user_content.startswith(expected_user_content), "Content for user.conf does not match expected UTF-8."