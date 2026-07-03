# test_final_state.py

import os
import ast
import subprocess
import pytest

def test_makefile_fixed():
    makefile_path = "/home/user/legacy/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}"

    with open(makefile_path, "r") as f:
        lines = f.readlines()

    # Check that gcc line uses a tab instead of spaces
    has_tab = any(line.startswith("\tgcc") for line in lines)
    assert has_tab, "Makefile must use a tab character for the compilation command recipe."

    content = "".join(lines)
    # Check for conditional flag
    assert "ALT" in content and "-DALT_POLY" in content, "Makefile must support conditional builds with ALT=1 passing -DALT_POLY to gcc."

def test_validator_python3():
    validator_path = "/home/user/legacy/validator.py"
    assert os.path.isfile(validator_path), f"Python script missing at {validator_path}"

    with open(validator_path, "r") as f:
        content = f.read()

    # Check if it's valid Python 3 syntax
    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"{validator_path} contains invalid Python 3 syntax: {e}")

    # Check that Python 2 specific built-ins are removed
    assert "xrange" not in content, "The script still uses Python 2 'xrange'."
    assert 'print "' not in content, "The script still uses Python 2 'print' statement syntax."

def test_result_txt():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file missing at {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    # The expected output is calculated as:
    # ASCII sum of "MigrationTest2023" = 1553
    # With ALT_POLY, sum starts at 42. Total = 1595.
    # 1595 % 256 = 59
    # Sum of 0 to 58 = 1711
    assert content == "Result: 1711", f"Expected 'Result: 1711', but found '{content}' in {result_path}"