# test_final_state.py

import os
import ast
import re
import ctypes
import importlib.util
import pytest

VALIDATOR_PATH = '/home/user/validator.py'
TEST_VALIDATOR_PATH = '/home/user/test_validator.py'
TEST_OUTPUT_PATH = '/home/user/test_output.txt'

def test_validator_py_exists():
    assert os.path.isfile(VALIDATOR_PATH), f"The file {VALIDATOR_PATH} does not exist."

def test_test_validator_py_exists():
    assert os.path.isfile(TEST_VALIDATOR_PATH), f"The file {TEST_VALIDATOR_PATH} does not exist."

def test_test_output_txt_exists_and_passed():
    assert os.path.isfile(TEST_OUTPUT_PATH), f"The file {TEST_OUTPUT_PATH} does not exist."
    with open(TEST_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for pytest success string like "3 passed"
    assert re.search(r'\d+ passed', content), "The test output does not indicate successful test passes (e.g., '3 passed')."

def test_test_validator_contains_required_functions():
    with open(TEST_VALIDATOR_PATH, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=TEST_VALIDATOR_PATH)

    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    required_functions = {'test_valid_token', 'test_invalid_format', 'test_invalid_checksum'}

    missing = required_functions - functions
    assert not missing, f"The test suite is missing the following required functions: {missing}"

def test_validator_py_logic_and_ctypes():
    # Load the updated validator.py
    spec = importlib.util.spec_from_file_location("validator", VALIDATOR_PATH)
    assert spec is not None, "Could not load validator.py"
    validator = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(validator)
    except Exception as e:
        pytest.fail(f"Failed to execute {VALIDATOR_PATH}. Is it valid Python 3 code? Error: {e}")

    # 1. Check argtypes and restype
    assert hasattr(validator, 'lib'), "validator.py does not define 'lib'"
    compute_hash = validator.lib.compute_hash

    assert compute_hash.argtypes == [ctypes.c_char_p, ctypes.c_int], "lib.compute_hash.argtypes is not correctly set."
    assert compute_hash.restype == ctypes.c_uint32, "lib.compute_hash.restype is not correctly set."

    # 2. Check get_checksum encodes string to bytes
    # If it doesn't encode, calling it with a str in Python 3 will raise ctypes.ArgumentError
    try:
        checksum = validator.get_checksum("admin123")
    except ctypes.ArgumentError:
        pytest.fail("get_checksum raised ctypes.ArgumentError. Did you forget to encode the string to bytes?")
    except Exception as e:
        pytest.fail(f"get_checksum failed with an unexpected error: {e}")

    # Calculate expected hash for "admin123" to verify correctness
    # DJB2: hash = 5381; hash = ((hash << 5) + hash) + c
    expected_hash = 5381
    for c in b"admin123":
        expected_hash = ((expected_hash << 5) + expected_hash + c) & 0xFFFFFFFF

    assert checksum == expected_hash, f"get_checksum returned {checksum}, expected {expected_hash}."

    # 3. Check parse_token and validate
    tv = validator.TokenValidator()

    # Valid token
    valid_token = f"SECadmin123#{expected_hash:08x}"
    assert tv.validate(valid_token) is True, "TokenValidator failed to validate a correct token."

    # Invalid checksum
    invalid_checksum_token = "SECadmin123#00000000"
    assert tv.validate(invalid_checksum_token) is False, "TokenValidator incorrectly validated a token with a bad checksum."

    # Invalid format
    with pytest.raises(ValueError):
        tv.parse_token("BADadmin123#00000000")
    with pytest.raises(ValueError):
        tv.parse_token("SECadmin123")