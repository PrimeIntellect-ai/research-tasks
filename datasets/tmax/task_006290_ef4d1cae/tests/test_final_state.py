# test_final_state.py
import os
import json
import subprocess
import base64
import pytest

PROJECT_DIR = "/home/user/project"

def test_evaluator_executable_exists_and_runs():
    executable_path = os.path.join(PROJECT_DIR, "evaluator")
    assert os.path.isfile(executable_path), f"Executable {executable_path} not found."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

    # Check if it runs and produces expected output
    try:
        # We run it with a simple expression to ensure it's dynamically linked correctly
        # and finds libexpr.so (which means rpath or LD_LIBRARY_PATH is correct).
        result = subprocess.run(
            [executable_path, "3 4 +"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        assert result.stdout.strip() == "7", f"Expected evaluator to output '7' for '3 4 +', got '{result.stdout.strip()}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running evaluator failed with error: {e.stderr}. This might indicate a missing shared library or linking issue.")

def test_v2_schema_json_correctness():
    v1_path = os.path.join(PROJECT_DIR, "v1_schema.txt")
    v2_path = os.path.join(PROJECT_DIR, "v2_schema.json")

    assert os.path.isfile(v1_path), f"File {v1_path} is missing."
    assert os.path.isfile(v2_path), f"File {v2_path} is missing. The migration step was not completed."

    with open(v1_path, "r") as f:
        v1_lines = f.read().splitlines()

    expected_data = []
    for line in v1_lines:
        if not line.strip():
            continue
        decoded_expr = base64.b64decode(line).decode("utf-8").strip()

        # Evaluate using a simple python stack to find expected value
        stack = []
        for char in decoded_expr:
            if char.isdigit():
                stack.append(int(char))
            elif char == '+':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif char == '-':
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            elif char == '*':
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)

        expected_data.append({
            "expression": decoded_expr,
            "value": stack[0] if stack else 0
        })

    with open(v2_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {v2_path} is not strictly valid JSON.")

    assert isinstance(actual_data, list), "The root of v2_schema.json must be a JSON array."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} items in v2_schema.json, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} in v2_schema.json is not a JSON object."
        assert "expression" in actual, f"Item at index {i} is missing the 'expression' key."
        assert "value" in actual, f"Item at index {i} is missing the 'value' key."
        assert actual["expression"] == expected["expression"], f"Expected expression '{expected['expression']}' at index {i}, got '{actual['expression']}'."
        assert actual["value"] == expected["value"], f"Expected value {expected['value']} at index {i}, got {actual['value']}."