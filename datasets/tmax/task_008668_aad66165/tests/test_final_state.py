# test_final_state.py

import os
import sys
import threading
import importlib.util
import pytest

SECRET_FILE = "/home/user/secret.txt"
PARSER_FILE = "/home/user/ticket_4099/parser.py"
EXPECTED_SECRET = "sk_bkp_8f92a1b7c6d5e4f3g2h1i0j"

def test_secret_recovered():
    assert os.path.exists(SECRET_FILE), f"Secret file {SECRET_FILE} does not exist."
    with open(SECRET_FILE, "r") as f:
        content = f.read().strip()
    assert EXPECTED_SECRET in content, f"The recovered secret in {SECRET_FILE} is incorrect."

def test_parser_exists():
    assert os.path.isfile(PARSER_FILE), f"Parser file {PARSER_FILE} does not exist."

def test_parser_fixed():
    # Dynamically import the parser module
    spec = importlib.util.spec_from_file_location("parser", PARSER_FILE)
    assert spec is not None, "Could not load parser spec."
    parser_module = importlib.util.module_from_spec(spec)
    sys.modules["parser"] = parser_module
    try:
        spec.loader.exec_module(parser_module)
    except Exception as e:
        pytest.fail(f"Failed to import {PARSER_FILE}: {e}")

    assert hasattr(parser_module, "extract_tags"), "extract_tags function missing in parser.py."
    extract_tags = parser_module.extract_tags

    # Test valid input
    try:
        valid_result = extract_tags("[WARN] [DB] Timeout")
    except Exception as e:
        pytest.fail(f"extract_tags raised an exception on valid input: {e}")

    assert valid_result == ["WARN", "DB"], f"extract_tags returned {valid_result} instead of ['WARN', 'DB'] on valid input."

    # Test malformed input (infinite loop protection and correct exception)
    result_container = {}

    def run_malformed():
        try:
            extract_tags("[ERROR] Unclosed bracket [")
            result_container['status'] = 'no_exception'
        except ValueError as e:
            if str(e) == "Malformed input":
                result_container['status'] = 'success'
            else:
                result_container['status'] = f'wrong_value_error: {e}'
        except Exception as e:
            result_container['status'] = f'wrong_exception: {type(e).__name__}'

    t = threading.Thread(target=run_malformed)
    t.daemon = True
    t.start()
    t.join(timeout=2.0)

    if t.is_alive():
        pytest.fail("extract_tags entered an infinite loop on malformed input (missing ']').")

    status = result_container.get('status', 'unknown')
    assert status == 'success', f"extract_tags failed on malformed input. Expected ValueError('Malformed input'), got: {status}"