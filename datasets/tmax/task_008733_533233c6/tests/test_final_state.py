# test_final_state.py

import os
import pytest

def test_setup_script_exists():
    assert os.path.isfile("/home/user/setup_microservice.sh"), "/home/user/setup_microservice.sh is missing"

def test_directories_exist():
    for d in ["/home/user/mail/inbox", "/home/user/mail/processed", "/home/user/mail/archive"]:
        assert os.path.isdir(d), f"Directory {d} is missing"

def test_groups_db_content():
    db_path = "/home/user/groups.db"
    assert os.path.isfile(db_path), f"{db_path} is missing"
    with open(db_path, "r") as f:
        content = f.read().strip()
    expected = "alice:admin\nbob:staff\ncharlie:guest"
    assert content == expected, f"{db_path} content does not match expected"

def test_c_program_exists():
    assert os.path.isfile("/home/user/mail_processor.c"), "/home/user/mail_processor.c is missing"
    assert os.path.isfile("/home/user/mail_processor"), "/home/user/mail_processor executable is missing"
    assert os.access("/home/user/mail_processor", os.X_OK), "/home/user/mail_processor is not executable"

def test_files_moved_correctly():
    # msg1 should be in processed
    assert os.path.isfile("/home/user/mail/processed/msg1.eml"), "msg1.eml was not moved to processed"

    # msg2 and msg3 should be in archive
    assert os.path.isfile("/home/user/mail/archive/msg2.eml"), "msg2.eml was not moved to archive"
    assert os.path.isfile("/home/user/mail/archive/msg3.eml"), "msg3.eml was not moved to archive"

    # inbox should not contain the original files
    assert not os.path.isfile("/home/user/mail/inbox/msg1.eml"), "msg1.eml still in inbox"
    assert not os.path.isfile("/home/user/mail/inbox/msg2.eml"), "msg2.eml still in inbox"
    assert not os.path.isfile("/home/user/mail/inbox/msg3.eml"), "msg3.eml still in inbox"

def test_processor_log_content():
    log_path = "/home/user/mail/processor.log"
    assert os.path.isfile(log_path), f"{log_path} is missing"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[2023-11-15 09:30:00] Processed email from alice (Group: admin)",
        "[2023-11-15 13:45:00] Processed email from charlie (Group: guest)",
        "[2023-11-15 20:15:00] Processed email from david (Group: unknown)"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected log entry '{expected}' not found in {log_path}"