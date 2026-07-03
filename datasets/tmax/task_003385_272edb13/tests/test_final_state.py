# test_final_state.py

import os
import pytest

def test_test_results_log_exists():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you save the output?"

def test_test_results_log_content():
    log_path = "/home/user/test_results.log"
    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "PASS: 2+3*4 = 14 (CRC: 187)",
        "PASS: 5*2+3 = 13 (CRC: 222)",
        "PASS: 1+1+1 = 3 (CRC: 26)"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {log_path}."

def test_makefile_fixed():
    makefile_path = "/home/user/pr_review/Makefile"
    assert os.path.isfile(makefile_path), f"File {makefile_path} does not exist."

    with open(makefile_path, "r") as f:
        lines = f.readlines()

    # Check that command lines start with a tab
    for line in lines:
        if line.strip().startswith("g++") or line.strip().startswith("rm"):
            assert line.startswith("\t"), "Makefile commands must start with a tab character."

def test_eval_crc_cpp_fixed():
    cpp_path = "/home/user/pr_review/eval_crc.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "0x07" in content and "0x70" not in content, "The CRC polynomial bug was not fixed (should be 0x07)."

    # Precedence bug
    assert "if (op == '*') return 2;" in content or "return 2" in content.split("if (op == '*')[")[0], "The operator precedence bug for '*' was not fixed."

    # Missing semicolon
    assert "};" in content or "}" in content, "The missing semicolon bug was not fixed."

def test_executable_exists():
    exe_path = "/home/user/pr_review/test_runner"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did you compile the project?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."