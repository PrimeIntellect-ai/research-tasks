# test_final_state.py

import os
import json
import re

def test_clean_logs_exists():
    assert os.path.isfile("/home/user/clean_logs.jsonl"), "The file /home/user/clean_logs.jsonl does not exist. Did you run the script?"

def test_clean_logs_line_count():
    with open("/home/user/raw_logs.jsonl", "r") as f:
        raw_lines = f.readlines()
    with open("/home/user/clean_logs.jsonl", "r") as f:
        clean_lines = f.readlines()

    assert len(clean_lines) == len(raw_lines), f"Expected {len(raw_lines)} lines in clean_logs.jsonl, but found {len(clean_lines)}."

def test_clean_logs_valid_json_and_transformations():
    with open("/home/user/raw_logs.jsonl", "r") as f:
        raw_lines = f.readlines()
    with open("/home/user/clean_logs.jsonl", "r") as f:
        clean_lines = f.readlines()

    for i, (raw_line, clean_line) in enumerate(zip(raw_lines, clean_lines)):
        try:
            clean_obj = json.loads(clean_line)
        except json.JSONDecodeError as e:
            assert False, f"Line {i+1} in clean_logs.jsonl is not valid JSON: {e}\nLine content: {clean_line.strip()}"

        # Fix the raw line's invalid \x escape sequences so we can parse it as truth
        fixed_raw_line = re.sub(r'\\x([0-9a-fA-F]{2})', r'\\u00\1', raw_line)
        raw_obj = json.loads(fixed_raw_line)

        # 1. Check user_id imputation
        if raw_obj.get("user_id") is None:
            assert clean_obj.get("user_id") == "UNKNOWN", f"Line {i+1}: 'user_id' was null but not imputed to 'UNKNOWN'."
        else:
            assert clean_obj.get("user_id") == raw_obj.get("user_id"), f"Line {i+1}: 'user_id' was altered improperly."

        # 2. Check email masking
        raw_email = raw_obj.get("email", "")
        if "@" in raw_email:
            domain = raw_email.split("@")[1]
            expected_email = f"***@{domain}"
            assert clean_obj.get("email") == expected_email, f"Line {i+1}: 'email' was not masked correctly. Expected {expected_email}, got {clean_obj.get('email')}."

        # 3. Check message (verifies unicode escape processing)
        assert clean_obj.get("message") == raw_obj.get("message"), f"Line {i+1}: 'message' was not processed correctly. Check escape sequence conversion."

        # 4. Check timestamp remains intact
        assert clean_obj.get("timestamp") == raw_obj.get("timestamp"), f"Line {i+1}: 'timestamp' was altered."