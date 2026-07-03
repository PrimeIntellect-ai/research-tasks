# test_final_state.py

import os
import subprocess
import json
import pytest

def test_inputs_json_recovered_and_fixed():
    path = "/home/user/math_toolkit/inputs.json"
    assert os.path.isfile(path), f"File {path} does not exist. Did you recover it?"

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {path} contains invalid JSON. Did you fix the syntax errors?")

    assert "numbers" in data, "JSON must contain a 'numbers' key."
    numbers = data["numbers"]
    assert isinstance(numbers, list), "'numbers' must be a list."

    expected_numbers = {15, 27, 42, 99, 1000}
    assert expected_numbers.issubset(set(numbers)), f"Expected numbers {expected_numbers} to be in the input JSON, got {numbers}."

def test_cargo_test_passes():
    repo_dir = "/home/user/math_toolkit"
    result = subprocess.run(
        ["cargo", "test"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"`cargo test` failed with output:\n{result.stdout}\n{result.stderr}"

def test_result_txt_exists_and_contains_output():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the program and redirect output?"

    with open(path, "r") as f:
        content = f.read()

    # Check for the expected collatz lengths of the numbers
    # 15 -> 17
    # 27 -> 111
    # 42 -> 8
    # 99 -> 25
    # 1000 -> 111
    expected_substrings = ["15", "27", "42", "99", "1000", "17", "111", "8", "25"]
    for sub in expected_substrings:
        assert sub in content, f"Expected to find '{sub}' in {path}, but it was missing. Content:\n{content}"