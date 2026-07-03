# test_final_state.py

import os
import pytest

CRACKED_PIN_PATH = "/home/user/cracked_pin.txt"
EXPECTED_PIN = "qzmp"

def test_cracked_pin_file_exists():
    assert os.path.isfile(CRACKED_PIN_PATH), f"The file {CRACKED_PIN_PATH} does not exist. Did you save the cracked PIN?"

def test_cracked_pin_content():
    with open(CRACKED_PIN_PATH, 'r') as f:
        content = f.read()

    assert content == EXPECTED_PIN, f"The content of {CRACKED_PIN_PATH} is incorrect. Expected '{EXPECTED_PIN}', but got '{content}'."