# test_final_state.py
import os
import pytest

def test_recovered_pin():
    pin_file = "/home/user/recovered_pin.txt"
    assert os.path.isfile(pin_file), f"File {pin_file} does not exist. The PIN was not saved."

    with open(pin_file, "r") as f:
        content = f.read().strip()

    assert content == "61942", f"The recovered PIN is incorrect. Expected '61942', got '{content}'."