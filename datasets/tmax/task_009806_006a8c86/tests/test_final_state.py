# test_final_state.py

import os
import json
import base64
import sys
import pytest

def get_expected_structure():
    return [
        {"4": [2, 2]},
        {"9": [3, 3]},
        {"25": [5, 5]},
        {"49": [7, 7]},
        {"121": [11, 11]}
    ]

def test_build_success_log():
    log_path = "/home/user/build_success.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist. The regression test might have failed or not written the output."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content, f"File {log_path} is empty."

    try:
        decoded_bytes = base64.b64decode(content)
        decoded_str = decoded_bytes.decode("utf-8")
    except Exception as e:
        pytest.fail(f"Content of {log_path} is not a valid UTF-8 base64 string: {e}")

    try:
        parsed_json = json.loads(decoded_str)
    except Exception as e:
        pytest.fail(f"Decoded content of {log_path} is not valid JSON: {e}")

    expected = get_expected_structure()
    assert parsed_json == expected, f"Parsed JSON from {log_path} does not match expected output.\nExpected: {expected}\nGot: {parsed_json}"

def test_regression_test_script():
    script_path = "/home/user/regression_test.py"
    assert os.path.exists(script_path), f"File {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "assert" in content, f"File {script_path} does not contain any 'assert' statements."
    assert "process_numbers" in content, f"File {script_path} does not seem to call 'process_numbers'."

def test_factorizer_functionality():
    module_path = "/home/user/math_build"
    assert os.path.exists(os.path.join(module_path, "factorizer.py")), "factorizer.py is missing."

    if module_path not in sys.path:
        sys.path.insert(0, module_path)

    try:
        import factorizer
    except ImportError as e:
        pytest.fail(f"Could not import factorizer: {e}")

    # Test functional correctness and encoding
    try:
        res = factorizer.process_numbers([4, 9, 25, 49, 121])
    except Exception as e:
        pytest.fail(f"process_numbers raised an exception: {e}")

    try:
        decoded_str = base64.b64decode(res).decode("utf-8")
        parsed = json.loads(decoded_str)
    except Exception as e:
        pytest.fail(f"Output of process_numbers is not valid base64 UTF-8 JSON: {e}")

    assert parsed == get_expected_structure(), "process_numbers did not return the expected mathematical results."

    # Test for race conditions with a larger set of numbers
    large_input = [i * i for i in range(2, 100)]
    try:
        res_large = factorizer.process_numbers(large_input)
        parsed_large = json.loads(base64.b64decode(res_large).decode("utf-8"))
    except Exception as e:
        pytest.fail(f"process_numbers failed on a larger input set: {e}")

    assert len(parsed_large) == len(large_input), "Concurrency bug is still present: missing results when processing many numbers."