# test_final_state.py

import os
import pytest

def test_peak_txt_exists_and_content():
    path = "/home/user/peak.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The Go program may not have run or failed to create the output."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "2.2461", f"Expected dominant frequency to be '2.2461', but got '{content}' in {path}."

def test_go_main_exists():
    path = "/home/user/synth_data/main.go"
    assert os.path.isfile(path), f"Go source file {path} does not exist."