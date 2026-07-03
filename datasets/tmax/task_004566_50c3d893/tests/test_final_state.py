# test_final_state.py

import os
import pytest

def test_target_file_log():
    path = "/home/user/target_file.log"
    assert os.path.isfile(path), f"Missing target file log at {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "/home/user/.hidden_kernel_module"
    assert content == expected, f"Expected {path} to contain '{expected}', but found '{content}'"

def test_payload_log():
    path = "/home/user/payload.log"
    assert os.path.isfile(path), f"Missing payload log at {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "MALICIOUS_INJECT_X86_64"
    assert content == expected, f"Expected {path} to contain '{expected}', but found '{content}'"

def test_minimized_input_txt():
    path = "/home/user/minimized_input.txt"
    assert os.path.isfile(path), f"Missing minimized input file at {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "CONFIG_OPT_8891=TRUE"
    assert content == expected, f"Expected {path} to contain '{expected}', but found '{content}'"