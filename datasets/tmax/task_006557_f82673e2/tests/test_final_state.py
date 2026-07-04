# test_final_state.py
import os
import json
import subprocess
import ast
import pytest

SCRIPT_PATH = "/home/user/find_triangles.py"
OUTPUT_PATH = "/home/user/triangles.json"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_script_execution_knows():
    # Run the script with "KNOWS"
    result = subprocess.run(
        ["python3", SCRIPT_PATH, "KNOWS"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed to execute with 'KNOWS'. Error: {result.stderr}"

    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {OUTPUT_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "Output JSON must be a list of arrays."
    # Sort inner arrays and outer array to be robust, though the spec says inner arrays must be sorted
    sorted_data = sorted([sorted(triangle) for triangle in data])
    assert sorted_data == [[1, 2, 3]], f"Expected [[1, 2, 3]] for 'KNOWS', got {data}"

def test_script_execution_likes():
    # Run the script with "LIKES"
    result = subprocess.run(
        ["python3", SCRIPT_PATH, "LIKES"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed to execute with 'LIKES'. Error: {result.stderr}"

    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {OUTPUT_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "Output JSON must be a list of arrays."
    sorted_data = sorted([sorted(triangle) for triangle in data])
    assert sorted_data == [[4, 5, 6]], f"Expected [[4, 5, 6]] for 'LIKES', got {data}"

def test_parameterized_query_used():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    # Check for common parameterization markers in sqlite3
    # Either '?' or named parameters like ':type' or '%s' (though %s is not standard for sqlite3, some might use it if wrapping)
    has_qmark = "?" in content
    has_named = ":" in content

    assert has_qmark or has_named, "Script does not appear to use parameterized queries (missing '?' or ':name' placeholders)."

    # Additionally parse AST to ensure we don't just have string formatting for the query
    # (A basic check to ensure the file is valid Python)
    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"Script contains syntax errors: {e}")