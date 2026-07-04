# test_final_state.py

import os
import pytest

def test_script_exists():
    script_path = "/home/user/process_logs.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_script_uses_streaming():
    script_path = "/home/user/process_logs.py"
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check that it doesn't use .read() or .readlines()
    assert ".read()" not in content, "The script should not load the entire file into memory using .read()."
    assert ".readlines()" not in content, "The script should not load the entire file into memory using .readlines()."

def test_output_file_exists():
    output_path = "/home/user/clean_inserts.sql"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_output_file_contents():
    output_path = "/home/user/clean_inserts.sql"
    expected_lines = [
        "INSERT INTO user_activity (event_time, ip_address, user_email) VALUES ('2023-10-12 08:23:45', '192.168.1.100', 'alice@example.com');",
        "INSERT INTO user_activity (event_time, ip_address, user_email) VALUES ('2023-10-12 08:25:01', '172.16.254.1', 'bob.smith@domain.co.uk');",
        "INSERT INTO user_activity (event_time, ip_address, user_email) VALUES ('2023-10-12 08:30:00', '8.8.8.8', 'charlie@company.com');",
        "INSERT INTO user_activity (event_time, ip_address, user_email) VALUES ('2023-10-12 09:05:22', '127.0.0.1', 'admin@localhost');"
    ]

    with open(output_path, 'r', encoding='utf-8') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} statements, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i + 1}.\nExpected: {expected}\nActual: {actual}"