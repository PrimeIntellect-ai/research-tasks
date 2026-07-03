# test_final_state.py

import os
import json
import re

def test_vectors_json_recovered():
    path = '/home/user/physics/vectors.json'
    assert os.path.isfile(path), f"{path} was not recovered."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{path} does not contain valid JSON."

    assert isinstance(data, list), "vectors.json should contain a list of test cases."
    assert len(data) == 3, "vectors.json should contain exactly 3 test cases."
    assert data[0].get("expected") == 2.0, "The recovered vectors.json content is incorrect."
    assert data[1].get("expected") == 2.5, "The recovered vectors.json content is incorrect."

def test_calc_go_fixed():
    path = '/home/user/physics/calc.go'
    assert os.path.isfile(path), f"{path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    # Check for corrected formula
    assert re.search(r'positions\[\w+\]\s*\*\s*weights\[\w+\]|weights\[\w+\]\s*\*\s*positions\[\w+\]', content), \
        "The formula in calc.go was not corrected to multiply positions by weights."

    # Check for updated function signature
    assert re.search(r'func\s+CalculateCenterOfMass\s*\(.*?\)\s*\(\s*float64\s*,\s*error\s*\)', content), \
        "The CalculateCenterOfMass function signature was not updated to return (float64, error)."

    # Check that panic is removed and error is returned
    assert "panic(" not in content, "The panic statement was not removed from calc.go."
    assert "zero weight sum" in content, "The 'zero weight sum' error message is missing."
    assert re.search(r'return\s+0(?:\.0)?\s*,\s*(?:errors\.New|fmt\.Errorf)', content), \
        "The code does not return 0.0 and an error when total weight is zero."

def test_test_results_log():
    path = '/home/user/physics/test_results.log'
    assert os.path.isfile(path), f"{path} was not created."

    with open(path, 'r') as f:
        content = f.read().lower()

    assert "pass" in content, "The test_results.log does not indicate passing tests."
    assert "fuzz" in content, "The test_results.log does not indicate that fuzzing was executed."