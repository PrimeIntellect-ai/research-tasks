# test_final_state.py

import os
import pytest

def test_result_log_exists_and_correct():
    path = "/home/user/result.log"
    assert os.path.isfile(path), f"File {path} does not exist. The Go program might not have been run or did not write to the correct file."

    with open(path, "r") as f:
        content = f.read()

    assert content == "CRITICAL", f"Expected content 'CRITICAL' in {path}, but got '{content}'."

def test_parser_go_fixes():
    path = "/home/user/parser.go"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "os.Readfile" not in content, "The compiler bug (os.Readfile) is still present in parser.go."
    assert "os.ReadFile" in content, "The compiler bug was not correctly fixed to os.ReadFile."

    assert "6+length+1" not in content.replace(" ", ""), "The off-by-one bug (6+length+1) is still present in parser.go."