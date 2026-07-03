# test_final_state.py

import os
import math

def test_fuzzer_script_exists_and_non_empty():
    fuzzer_path = "/home/user/geo_project/fuzzer.py"
    assert os.path.isfile(fuzzer_path), f"The fuzzer script was not found at {fuzzer_path}."
    assert os.path.getsize(fuzzer_path) > 0, "The fuzzer script is empty."

    with open(fuzzer_path, "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, "The fuzzer script only contains whitespace."

def test_success_txt_exists_and_correct():
    success_path = "/home/user/geo_project/success.txt"
    assert os.path.isfile(success_path), f"The file {success_path} does not exist. Did you run verify.py?"

    test_vals = [1e-9, 1e-8, 1e-7, 1.0, 3.14]
    expected_lines = [f"{2.0 * math.sin(t / 2.0):.12e}" for t in test_vals]

    with open(success_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in success.txt, got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i+1} of success.txt: expected {expected}, got {actual}."

def test_assertions_in_geo_math():
    geo_math_path = "/home/user/geo_project/geo_math.py"
    assert os.path.isfile(geo_math_path), f"The file {geo_math_path} does not exist."

    with open(geo_math_path, "r") as f:
        content = f.read()

    assert 'assert isinstance(theta, float), "theta must be a float"' in content, "Missing or incorrect type assertion in geo_math.py."
    assert 'assert theta >= 0.0, "theta must be non-negative"' in content, "Missing or incorrect value assertion in geo_math.py."