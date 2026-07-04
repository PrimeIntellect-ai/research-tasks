# test_final_state.py

import os
import re
import pytest

def test_recovered_data_directory_exists():
    target_dir = "/home/user/recovered_data"
    assert os.path.exists(target_dir), f"The target directory {target_dir} does not exist. The expect script may not have run successfully."
    assert os.path.isdir(target_dir), f"The path {target_dir} is not a directory."

def test_restore_activity_log_exists():
    log_path = "/home/user/restore_activity.log"
    assert os.path.exists(log_path), f"The log file {log_path} does not exist. Ensure the expect script was executed successfully."
    assert os.path.isfile(log_path), f"The path {log_path} is not a file."

def test_restored_files_txt_content():
    txt_path = "/home/user/restored_files.txt"
    assert os.path.exists(txt_path), f"The file {txt_path} does not exist."
    assert os.path.isfile(txt_path), f"The path {txt_path} is not a file."

    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/recovered_data/config.yml",
        "/home/user/recovered_data/database.db",
        "/home/user/recovered_data/images.tar.gz"
    ]

    assert lines == expected_lines, f"The contents of {txt_path} do not match the expected file paths. Found: {lines}"

def test_logrotate_conf():
    conf_path = "/home/user/test_logrotate.conf"
    assert os.path.exists(conf_path), f"The file {conf_path} does not exist."
    assert os.path.isfile(conf_path), f"The path {conf_path} is not a file."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "/home/user/restore_activity.log" in content, f"The logrotate config does not specify the target log file '/home/user/restore_activity.log'."

    required_directives = [
        r"\bdaily\b",
        r"\brotate\s+5\b",
        r"\bcompress\b",
        r"\bmissingok\b",
        r"\bcreate\s+0644\s+user\s+user\b"
    ]

    for directive in required_directives:
        assert re.search(directive, content), f"The logrotate config is missing or has an incorrect directive matching regex: {directive}"