# test_final_state.py
import os
import json
import pytest
from fractions import Fraction

BASE_DIR = "/home/user/vector_api"

def test_c_engine_patched():
    c_file = os.path.join(BASE_DIR, "vector_math.c")
    assert os.path.isfile(c_file), f"File {c_file} is missing."

    with open(c_file, "r") as f:
        content = f.read()

    assert "%d/%u" in content, "The C engine vector_math.c does not appear to be patched. Missing '%d/%u' in sscanf."
    assert "%u/%u" not in content, "The C engine vector_math.c still contains the buggy '%u/%u' sscanf format."

def test_shared_library_built():
    so_file = os.path.join(BASE_DIR, "libvector.so")
    assert os.path.isfile(so_file), f"Shared library {so_file} was not built."

def test_integration_script_exists():
    py_file = os.path.join(BASE_DIR, "test_integration.py")
    assert os.path.isfile(py_file), f"Integration script {py_file} is missing."

def test_results_json_correct():
    test_cases_file = os.path.join(BASE_DIR, "test_cases.json")
    results_file = os.path.join(BASE_DIR, "test_results.json")

    assert os.path.isfile(test_cases_file), f"Test cases file {test_cases_file} is missing."
    assert os.path.isfile(results_file), f"Results file {results_file} is missing."

    with open(test_cases_file, "r") as f:
        test_cases = json.load(f)

    expected_results = {}
    for case_id, data in test_cases.items():
        v1_str = data["v1"].split("]", 1)[-1].strip()
        v2_str = data["v2"].split("]", 1)[-1].strip()

        v1_parts = v1_str.split()
        v2_parts = v2_str.split()

        total = Fraction(0)
        for p1, p2 in zip(v1_parts, v2_parts):
            total += Fraction(p1) * Fraction(p2)

        expected_results[case_id] = f"{total.numerator}/{total.denominator}"

    with open(results_file, "r") as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Results file {results_file} is not valid JSON.")

    assert actual_results == expected_results, f"Results in {results_file} do not match the expected math output. Expected: {expected_results}, Actual: {actual_results}"