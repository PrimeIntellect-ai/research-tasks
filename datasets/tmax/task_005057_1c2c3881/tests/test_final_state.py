# test_final_state.py
import os
import pytest

def test_validator_rs_fixed():
    file_path = "/home/user/polyglot/validator.rs"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()

    # A simple check to ensure the lifetime issue is mitigated
    # Either the function returns an owned String, or the reference logic is changed.
    assert "fn get_token<'a>() -> &'a str" not in content or "String::from" not in content, \
        "validator.rs still appears to return a borrowed reference to a local variable."

def test_parser_c_fixed():
    file_path = "/home/user/polyglot/parser.c"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()

    assert "strcpy(" not in content, "parser.c still contains the vulnerable strcpy function."
    assert "strncpy(" in content, "parser.c does not use the secure strncpy function."

def test_logger_go_fixed():
    file_path = "/home/user/polyglot/logger.go"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()

    assert "Mutex" in content, "logger.go does not use a Mutex to prevent race conditions."

def test_build_output_log_exists_and_correct():
    file_path = "/home/user/build_output.log"
    assert os.path.isfile(file_path), f"The file {file_path} is missing. The gateway script may not have been run or failed to verify the token."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert "BUILD_AND_SECURE_COMPLETE" in content, \
        f"The build_output.log does not contain the expected success message. Found: {content}"