# test_final_state.py

import os
import subprocess
import pytest

def test_magic_txt():
    path = "/home/user/magic.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "Z3R0", f"Expected magic.txt to contain 'Z3R0', but got '{content}'."

def test_parser_go_fixes():
    path = "/home/user/parser/parser.go"
    assert os.path.isfile(path), f"Expected Go source file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check for bounds check returning "invalid length"
    assert "invalid length" in content, "Expected parser.go to return 'invalid length' error for bounds check."

    # Check for Mutex usage
    assert "Mutex" in content, "Expected parser.go to use sync.Mutex or sync.RWMutex."
    assert ".Lock()" in content, "Expected parser.go to lock the mutex."
    assert ".Unlock()" in content, "Expected parser.go to unlock the mutex."

def test_parser_test_go():
    path = "/home/user/parser/parser_test.go"
    assert os.path.isfile(path), f"Expected test file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "func TestParserRegression" in content, "Expected parser_test.go to contain func TestParserRegression(t *testing.T)."

def test_go_test_race():
    parser_dir = "/home/user/parser"
    assert os.path.isdir(parser_dir), f"Expected directory {parser_dir} does not exist."

    result = subprocess.run(
        ["go", "test", "-race"],
        cwd=parser_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"'go test -race' failed with output:\n{result.stdout}\n{result.stderr}"