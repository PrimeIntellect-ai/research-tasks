# test_final_state.py

import os
import subprocess
import ast
import pytest

def test_modern_math_eval_exists():
    path = "/home/user/modern/math_eval.py"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_output_file_contents():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file {path} was not created."

    expected_lines = [
        "Expression: + 3 4 | Result: 7 | Checksum: 284242851",
        "Expression: - 10 * 2 3 | Result: 4 | Checksum: 3514757530",
        "Expression: / 10 3 | Result: 3 | Checksum: 216744030",
        "Expression: + / 20 6 * 2 5 | Result: 13 | Checksum: 2603831737"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The contents of output.txt do not match the expected output format or mathematical results."

def test_math_test_fixture_runs():
    path = "/home/user/modern/test_math.py"
    assert os.path.isfile(path), f"Test fixture {path} does not exist."

    # Run the unittest
    result = subprocess.run(
        ["python3", "-m", "unittest", path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Unittest failed to run successfully:\n{result.stderr}\n{result.stdout}"

def test_math_eval_code_fixes():
    path = "/home/user/modern/math_eval.py"
    with open(path, "r") as f:
        source = f.read()

    # Check for Python 3 syntax validity
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"math_eval.py has invalid Python 3 syntax: {e}")

    # Verify integer division is preserved (either // or int(/))
    has_floor_div = "//" in source
    has_int_cast = "int(" in source
    assert has_floor_div or has_int_cast, "math_eval.py must use floor division (//) or int() casting to preserve legacy division behavior."

    # Verify FFI string encoding
    has_encode = ".encode" in source or "bytes(" in source
    assert has_encode, "math_eval.py must encode the string to bytes before passing it to the C function."