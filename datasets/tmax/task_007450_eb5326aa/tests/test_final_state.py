# test_final_state.py

import os
import pytest

def test_recovered_event_file_exists():
    path = "/home/user/recovered_event.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The decoded event string was not saved."

def test_recovered_event_content():
    path = "/home/user/recovered_event.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected = "CRITICAL_FAILURE_AT_NODE_77"
    assert content == expected, f"Expected the recovered event to be '{expected}', but got '{content}'."

def test_parser_script_recovered():
    path = "/home/user/parser.py"
    assert os.path.isfile(path), f"File {path} does not exist. The python script was not recovered from the memdump."

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    assert "def decode(" in content, "The recovered parser.py does not contain the expected 'decode' function."