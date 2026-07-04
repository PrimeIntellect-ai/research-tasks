# test_final_state.py

import os
import stat
import pytest

def test_audit_token_correct():
    """Verify that the extracted audit token is exactly correct."""
    token_file = "/home/user/audit_token.txt"
    assert os.path.isfile(token_file), f"{token_file} does not exist."

    with open(token_file, "r") as f:
        content = f.read()

    expected_token = "555345523d61756469746f723b5045524d3d4752414e545f4155444954"
    assert content == expected_token, f"The content of {token_file} is incorrect or contains extra whitespace/newlines. Expected: {expected_token}, Got: {repr(content)}"

def test_parser_cpp_exists():
    """Verify that the C++ source file exists."""
    cpp_file = "/home/user/parser.cpp"
    assert os.path.isfile(cpp_file), f"{cpp_file} does not exist."

def test_parser_executable_exists():
    """Verify that the compiled parser executable exists and is executable."""
    exe_file = "/home/user/parser"
    assert os.path.isfile(exe_file), f"{exe_file} does not exist."

    st = os.stat(exe_file)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"{exe_file} is not marked as executable."

def test_api_dump_txt_exists():
    """Verify that the decrypted API dump exists and contains expected HTTP traffic."""
    dump_file = "/home/user/api_dump.txt"
    assert os.path.isfile(dump_file), f"{dump_file} does not exist."

    with open(dump_file, "r", errors="ignore") as f:
        content = f.read()

    assert "GET /api/v1" in content, f"{dump_file} does not appear to be correctly decrypted (missing expected HTTP requests)."
    assert "Authorization: Bearer" in content, f"{dump_file} does not contain Authorization headers."