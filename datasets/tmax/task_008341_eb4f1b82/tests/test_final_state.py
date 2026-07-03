# test_final_state.py
import os
import json
import re

def test_evaluator_c_fixed():
    path = "/home/user/evaluator.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check for memory allocation fix
    # The student might write malloc(strlen(expr) + 1) or similar
    assert re.search(r"malloc\s*\(\s*strlen\s*\(\s*expr\s*\)\s*\+\s*1\s*\)", content) or \
           re.search(r"malloc\s*\(\s*1\s*\+\s*strlen\s*\(\s*expr\s*\)\s*\)", content) or \
           re.search(r"strdup\s*\(\s*expr\s*\)", content) or \
           re.search(r"calloc\s*\(", content), \
           f"Buffer allocation bug not fixed in {path} (expected malloc(strlen(expr) + 1) or equivalent)."

    # Check for memory leak fix
    assert re.search(r"free\s*\(\s*expr_copy\s*\)", content), f"Memory leak not fixed in {path} (expected free(expr_copy))."

def test_libeval_so_exists():
    path = "/home/user/libeval.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist."

def test_output_json():
    path = "/home/user/output.json"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{path} is not a valid JSON file."

    expected_data = {
        "3 4 + 2 *": {
            "checksum": 140,
            "result": 14.0
        },
        "5 2 * 3 +": {
            "checksum": 141,
            "result": 13.0
        },
        "10 5 * 20 + 2 *": {
            "checksum": 204,
            "result": 140.0
        }
    }

    assert isinstance(data, dict), f"Expected JSON root to be a dictionary."

    for expr, expected_values in expected_data.items():
        assert expr in data, f"Expression '{expr}' missing from {path}."

        actual_checksum = data[expr].get("checksum")
        expected_checksum = expected_values["checksum"]
        assert actual_checksum == expected_checksum, \
            f"Checksum for '{expr}' is incorrect. Expected {expected_checksum}, got {actual_checksum}."

        actual_result = data[expr].get("result")
        expected_result = expected_values["result"]
        assert isinstance(actual_result, (int, float)), \
            f"Result for '{expr}' must be a number."
        assert abs(actual_result - expected_result) < 1e-6, \
            f"Result for '{expr}' is incorrect. Expected {expected_result}, got {actual_result}."