# test_final_state.py

import os
import json
import subprocess
import ast

def test_debugging_results_json_exists():
    assert os.path.isfile("/home/user/debugging_results.json"), "The file /home/user/debugging_results.json does not exist."

def test_debugging_results_json_format():
    with open("/home/user/debugging_results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/debugging_results.json is not valid JSON."

    expected_keys = {"bad_commit", "minimized_log_line", "corrected_formula_code"}
    assert set(data.keys()) == expected_keys, f"JSON must contain exactly the keys: {expected_keys}"

def test_bad_commit_hash():
    with open("/home/user/debugging_results.json", "r") as f:
        data = json.load(f)

    repo_dir = "/home/user/log_processor"

    # Find the commit hash for "Optimize apdex calculation"
    result = subprocess.run(
        ["git", "log", "--grep=Optimize apdex calculation", "--format=%H"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    expected_hash = result.stdout.strip()

    assert expected_hash != "", "Could not find the expected bad commit in the git history."
    assert data["bad_commit"] == expected_hash, f"Incorrect bad_commit. Expected {expected_hash}, got {data['bad_commit']}"

def test_minimized_log_line():
    with open("/home/user/debugging_results.json", "r") as f:
        data = json.load(f)

    expected_line = "2023-11-01 12:00 INFO 80 15 100"
    assert data["minimized_log_line"].strip() == expected_line, f"Incorrect minimized_log_line. Expected '{expected_line}'"

def test_corrected_formula_code():
    with open("/home/user/debugging_results.json", "r") as f:
        data = json.load(f)

    formula_code = data["corrected_formula_code"]

    # We will evaluate the formula with some test variables to ensure it is mathematically correct
    test_env = {
        "satisfied": 80,
        "tolerating": 15,
        "total": 100
    }

    # The expected result is (80 + 15/2.0) / 100 = 0.875
    expected_result = 0.875

    # Try to execute the student's line of code
    # Assuming it's something like `apdex = (satisfied + (tolerating / 2.0)) / total`
    # We can execute it in the test_env
    try:
        exec(formula_code, {}, test_env)
    except Exception as e:
        assert False, f"Failed to execute corrected_formula_code: {e}"

    # If they assigned to a variable, let's find it. Usually it's 'apdex'
    if "apdex" in test_env:
        result = test_env["apdex"]
    else:
        # If they just provided the expression, let's try evaluating it
        try:
            result = eval(formula_code, {}, test_env)
        except Exception as e:
            assert False, f"Could not determine the result of the formula. Ensure it assigns to 'apdex' or is a pure expression. Error: {e}"

    assert abs(result - expected_result) < 1e-6, f"The corrected formula yielded {result}, but expected {expected_result}."