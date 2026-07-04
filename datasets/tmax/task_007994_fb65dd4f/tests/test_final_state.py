# test_final_state.py

import os
import pytest

def test_pin_file_correct():
    pin_path = '/home/user/pin.txt'
    assert os.path.isfile(pin_path), f"Expected file {pin_path} does not exist. Did you save the PIN?"

    with open(pin_path, 'r') as f:
        pin_content = f.read().strip()

    assert pin_content == "4821", f"The PIN in {pin_path} is incorrect. Expected '4821', got '{pin_content}'."

def test_decrypted_file_exists():
    # The task asks to save the decrypted plaintext to /home/user/decrypted.txt
    decrypted_path = '/home/user/decrypted.txt'
    assert os.path.isfile(decrypted_path), f"Expected file {decrypted_path} does not exist. Did you save the decrypted output?"

    with open(decrypted_path, 'r') as f:
        content = f.read()

    assert "C2_SERVER: evil-corp.local" in content, "The decrypted text does not contain expected C2_SERVER data."
    assert "4532111122223333" in content, "The decrypted text does not contain the expected credit card number."

def test_clean_report_correct():
    clean_path = '/home/user/clean_report.txt'
    assert os.path.isfile(clean_path), f"Expected file {clean_path} does not exist. Did you save the redacted output?"

    with open(clean_path, 'r') as f:
        content = f.read()

    expected_content = "C2_SERVER: evil-corp.local\nTARGET_CC: [REDACTED]\nSTATUS: ACTIVE\n"

    assert content.strip() == expected_content.strip(), (
        f"The content of {clean_path} does not match the expected redacted output.\n"
        f"Expected:\n{expected_content}\nGot:\n{content}"
    )

    assert "4532111122223333" not in content, "The 16-digit credit card number was not properly redacted in the clean report."