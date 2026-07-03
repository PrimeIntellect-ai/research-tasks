# test_final_state.py
import os
import json
import pytest
import re

BASE_DIR = "/home/user/fast-token-parser"
OUTPUT_FILE = "/home/user/parsed_tokens.json"

def test_parsed_tokens_json_exists_and_correct():
    assert os.path.isfile(OUTPUT_FILE), f"The output file {OUTPUT_FILE} was not generated."

    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {OUTPUT_FILE} does not contain valid JSON.")

    expected_data = [
        {"type": 1, "data": "hello"},
        {"error": "Invalid token"},
        {"type": 3, "data": "test"}
    ]

    assert data == expected_data, f"The contents of {OUTPUT_FILE} do not match the expected output. Got: {data}"

def test_test_suite_import_order():
    test_suite_path = os.path.join(BASE_DIR, "test_suite.py")
    assert os.path.isfile(test_suite_path), f"File {test_suite_path} is missing."

    with open(test_suite_path, "r") as f:
        content = f.read()

    import_config_idx = content.find("import config")
    import_ffi_idx = content.find("import ffi_wrapper")

    assert import_config_idx != -1, "'import config' is missing from test_suite.py"
    assert import_ffi_idx != -1, "'import ffi_wrapper' is missing from test_suite.py"

    assert import_config_idx < import_ffi_idx, "The import order is still incorrect. 'import config' must come before 'import ffi_wrapper'."

def test_parser_c_bounds_check():
    parser_path = os.path.join(BASE_DIR, "parser.c")
    assert os.path.isfile(parser_path), f"File {parser_path} is missing."

    with open(parser_path, "r") as f:
        content = f.read()

    # We are looking for a bounds check that involves 64. 
    # It could be `if (data_len > 64)`, `if(data_len>64)`, `if (64 < data_len)`, etc.
    # A simple regex to catch common valid fixes:
    has_check = re.search(r'data_len\s*>\s*64', content) or \
                re.search(r'64\s*<\s*data_len', content) or \
                re.search(r'data_len\s*>=\s*65', content) or \
                re.search(r'65\s*<=\s*data_len', content)

    assert has_check, "parser.c does not appear to contain a bounds check preventing data_len from exceeding 64 bytes."