# test_final_state.py

import os
import pytest

def test_analyze_go_exists():
    path = "/home/user/analyze.go"
    assert os.path.isfile(path), f"Missing file: {path}. You must create the Go program here."

def test_loot_txt_exists():
    path = "/home/user/loot.txt"
    assert os.path.isfile(path), f"Missing file: {path}. Your Go program should create this file."

def test_loot_txt_content():
    path = "/home/user/loot.txt"
    assert os.path.isfile(path), f"Cannot check content, missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "token_admin_9912",
        "token_user_7734"
    ]

    assert len(content) == len(expected), f"Expected {len(expected)} tokens in {path}, but found {len(content)}."

    for i, (actual, exp) in enumerate(zip(content, expected)):
        assert actual.strip() == exp, f"Line {i+1} in {path} is incorrect. Expected '{exp}', got '{actual.strip()}'."