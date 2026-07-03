# test_final_state.py

import os
import pytest

def test_c2_txt_exists_and_correct():
    c2_path = '/home/user/investigation/c2.txt'
    assert os.path.isfile(c2_path), f"The file {c2_path} does not exist. Did you save the extracted URL?"

    with open(c2_path, 'r') as f:
        content = f.read().strip()

    expected_url = "https://www.cample.com"
    assert content == expected_url, f"The content of {c2_path} is incorrect. Expected '{expected_url}', but got '{content}'."

def test_minimal_crash_txt_exists_and_correct():
    crash_path = '/home/user/investigation/minimal_crash.txt'
    assert os.path.isfile(crash_path), f"The file {crash_path} does not exist. Did you save the minimal crashing string?"

    with open(crash_path, 'r') as f:
        content = f.read().strip()

    # The minimal string to trigger the ValueError: Corrupt Header (length > 9000)
    # based on the regex `C2CFG\{(\d{4})\}(.*)` is exactly `C2CFG{9001}`
    expected_crash_string = "C2CFG{9001}"
    assert content == expected_crash_string, f"The content of {crash_path} is incorrect. Expected the minimal string '{expected_crash_string}', but got '{content}'."