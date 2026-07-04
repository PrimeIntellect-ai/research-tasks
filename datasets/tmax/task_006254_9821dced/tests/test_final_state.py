# test_final_state.py

import os
import json

def test_extracted_users_exists_and_correct():
    output_path = "/home/user/extracted_users.txt"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist. Did you run the script?"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_users = ["U1001", "U1002", "U1003", "U1004"]
    assert lines == expected_users, f"Expected extracted users to be {expected_users}, but got {lines}."

def test_incoming_logs_unmodified():
    input_path = "/home/user/incoming_logs.txt"
    assert os.path.isfile(input_path), f"Input file {input_path} is missing."

    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    expected_lines = [
        '{"event": {"user": {"id": "U1001", "role": "admin"}}}',
        '{"event": {"user": {"id": "U1002", "role": "user"}}}',
        '{"event": {"user": {"name": "Alice_No_ID"}}}',
        '{"event": {"user": {"id": "U1003", "role": "user"}}}',
        '{"event": "corrupted_payload_missing_braces"',
        '{"event": {"user": {"id": "U1004", "role": "guest"}}}'
    ]
    assert lines == expected_lines, "The incoming_logs.txt file was modified. You were instructed not to change the input file."