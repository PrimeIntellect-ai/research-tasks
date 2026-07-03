# test_final_state.py

import os
import json

def test_clean_logs_exists_and_correct():
    clean_logs_path = '/home/user/clean_logs.json'

    assert os.path.isfile(clean_logs_path), f"The file {clean_logs_path} does not exist."

    expected_data = [
        {"id": 1, "b64_payload": "U3lzdGVtIGJvb3RlZCBzdWNjZXNzZnVsbHk="},
        {"id": 2, "b64_payload": "Q3JpdGljYWwgZXJyb3I6IEFLZXkgaXMgZmFrZSBbUkVEQUNURURdIHVzZWQg"},
        {"id": 3, "b64_payload": "W1JFREFDVEVEXSBhbmQgW1JFREFDVEVEXQ=="}
    ]

    with open(clean_logs_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {clean_logs_path} does not contain valid JSON."

    assert actual_data == expected_data, f"The contents of {clean_logs_path} do not match the expected redacted state."

def test_final_output_exists_and_correct():
    final_output_path = '/home/user/final_output.log'

    assert os.path.isfile(final_output_path), f"The file {final_output_path} does not exist."

    expected_data = [
        {"id": 1, "b64_payload": "U3lzdGVtIGJvb3RlZCBzdWNjZXNzZnVsbHk="},
        {"id": 2, "b64_payload": "Q3JpdGljYWwgZXJyb3I6IEFLZXkgaXMgZmFrZSBbUkVEQUNURURdIHVzZWQg"},
        {"id": 3, "b64_payload": "W1JFREFDVEVEXSBhbmQgW1JFREFDVEVEXQ=="}
    ]

    with open(final_output_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {final_output_path} does not contain valid JSON."

    assert actual_data == expected_data, f"The contents of {final_output_path} do not match the expected redacted state."