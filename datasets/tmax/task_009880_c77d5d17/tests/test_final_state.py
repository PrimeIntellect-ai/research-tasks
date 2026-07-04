# test_final_state.py

import os
import ast
import re
import pytest

REPORT_PATH = "/home/user/report.txt"
APP_PATH = "/home/user/webapp/app.py"

def test_report_exists_and_content():
    assert os.path.exists(REPORT_PATH), f"{REPORT_PATH} does not exist. You must create the investigation report."

    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"{REPORT_PATH} must contain at least two lines."

    expected_file = "/home/user/webapp/app.py"
    assert lines[0] == expected_file, f"First line of report is incorrect. Expected '{expected_file}', got '{lines[0]}'."

    expected_cwe = "CWE-601"
    assert lines[1].upper() == expected_cwe, f"Second line of report is incorrect. Expected '{expected_cwe}', got '{lines[1]}'."

def test_app_py_fixed():
    assert os.path.exists(APP_PATH), f"{APP_PATH} does not exist."

    with open(APP_PATH, "r") as f:
        code = f.read()

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {APP_PATH}: {e}")

    # Check that there is some validation logic added
    # The prompt specifies checking for starts with single '/' and not '//' or 'http'
    # We can check for string methods like startswith, or urllib, or regex

    has_startswith = "startswith" in code
    has_urllib = "urllib.parse" in code or "urlparse" in code
    has_index_check = re.search(r"\[0\]", code) is not None
    has_regex = "re." in code or "match" in code
    has_in = " in " in code

    assert any([has_startswith, has_urllib, has_index_check, has_regex, has_in]), \
        "Could not find validation logic in app.py. Ensure you validate the 'next' parameter."

    # Ensure redirect is still being called
    redirect_called = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "redirect":
                redirect_called = True
                break

    assert redirect_called, "The 'redirect' function is no longer being called in app.py."