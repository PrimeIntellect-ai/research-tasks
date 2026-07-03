# test_final_state.py

import os
import pytest

def test_success_out_content():
    success_file = "/home/user/project/build/success.out"
    assert os.path.isfile(success_file), f"Expected output file {success_file} does not exist."

    with open(success_file, "r") as f:
        content = f.read().strip()

    expected_output = (
        "Application: MyApp\n"
        "Port: 8080\n"
        "Database Host: localhost\n"
        "Database User: admin"
    )

    assert content == expected_output, f"File {success_file} content does not match the expected output."

def test_config_h_valid():
    config_h_file = "/home/user/project/build/config.h"
    assert os.path.isfile(config_h_file), f"Generated header {config_h_file} does not exist."

    with open(config_h_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#define"):
            parts = line.strip().split()
            assert len(parts) >= 2, f"Invalid #define in {config_h_file}: {line}"
            macro_name = parts[1]
            assert macro_name != "#", f"Comment line was not ignored in {config_h_file}: {line}"
            assert macro_name != '""', f"Empty line was not ignored in {config_h_file}: {line}"

def test_codegen_logic_updated():
    codegen_file = "/home/user/project/src/codegen.cpp"
    assert os.path.isfile(codegen_file), f"File {codegen_file} does not exist."

    with open(codegen_file, "r") as f:
        content = f.read()

    # Check that the code contains some logic to handle '#' or empty lines
    has_hash_check = "('#')" in content or '"#"' in content or "'#'" in content
    has_empty_check = "empty()" in content or "length() == 0" in content or "size() == 0" in content or "pos == std::string::npos" in content or "find_first_not_of" in content

    assert has_hash_check or has_empty_check, "codegen.cpp does not appear to contain logic to skip comments or empty lines."