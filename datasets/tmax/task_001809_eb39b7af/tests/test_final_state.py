# test_final_state.py
import os
import base64

def test_payload_file_exists():
    assert os.path.isfile('/home/user/payload.txt'), "/home/user/payload.txt does not exist"

def test_payload_content():
    original = "<svg onload=alert(document.domain)>"
    reversed_str = original[::-1]
    expected_payload = base64.b64encode(reversed_str.encode()).decode()

    with open('/home/user/payload.txt', 'r') as f:
        actual_payload = f.read()

    assert actual_payload == expected_payload, (
        f"Content of /home/user/payload.txt is incorrect.\n"
        f"Expected: {expected_payload}\n"
        f"Actual: {actual_payload}\n"
        "Ensure there are no trailing newlines and the correct encoding sequence was applied."
    )