# test_final_state.py

import os
import subprocess
import pytest

def test_linux_binary_exists_and_elf():
    path = "/home/user/dist/sec-linux"
    assert os.path.isfile(path), f"Linux binary {path} is missing."

    with open(path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {path} is not a valid ELF executable."

def test_windows_binary_exists_and_pe():
    path = "/home/user/dist/sec-win.exe"
    assert os.path.isfile(path), f"Windows binary {path} is missing."

    with open(path, "rb") as f:
        magic = f.read(2)
    assert magic == b"MZ", f"File {path} is not a valid Windows PE executable."

def test_linux_binary_execution():
    path = "/home/user/dist/sec-linux"
    assert os.path.isfile(path), f"Linux binary {path} is missing."

    # Run with "ALLOW" which should return 0 and print "ALLOW"
    result = subprocess.run([path, "ALLOW"], capture_output=True, text=True)
    assert result.returncode == 0, f"Expected return code 0 for 'ALLOW', got {result.returncode}."
    assert "ALLOW" in result.stdout, f"Expected output to contain 'ALLOW', got {result.stdout}."

    # Run with empty or no args which should return 1
    result_empty = subprocess.run([path], capture_output=True, text=True)
    assert result_empty.returncode == 1, f"Expected return code 1 for missing args, got {result_empty.returncode}."

def test_test_props_py_exists_and_valid():
    path = "/home/user/test_props.py"
    assert os.path.isfile(path), f"Python test script {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "hypothesis" in content, f"Script {path} does not import hypothesis."
    assert "@given" in content, f"Script {path} does not use the @given decorator."

def test_test_result_log():
    path = "/home/user/test_result.log"
    assert os.path.isfile(path), f"Result log {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "TESTS_PASSED", f"Expected log to contain exactly 'TESTS_PASSED', got '{content}'."