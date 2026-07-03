# test_final_state.py

import os
import stat
import re
import pytest

def test_project_structure():
    assert os.path.isdir("/home/user/math_project"), "/home/user/math_project directory is missing"
    assert os.path.isdir("/home/user/math_project/src"), "/home/user/math_project/src directory is missing"
    assert os.path.isdir("/home/user/math_project/tests"), "/home/user/math_project/tests directory is missing"

    assert os.path.isfile("/home/user/math_project/src/parser.py"), "parser.py was not moved to src"
    assert os.path.isfile("/home/user/math_project/tests/test_parser.py"), "test_parser.py was not moved to tests"

    assert os.path.isfile("/home/user/math_project/src/__init__.py"), "src/__init__.py is missing"
    assert os.path.isfile("/home/user/math_project/tests/__init__.py"), "tests/__init__.py is missing"

def test_parser_fixed():
    with open("/home/user/math_project/src/parser.py", "r") as f:
        content = f.read()

    # The class level stack = [] should be removed or changed
    # We should look for an __init__ method that initializes self.stack
    assert re.search(r"def\s+__init__\s*\(\s*self\s*\)\s*:", content), "parser.py does not have an __init__ method"
    assert re.search(r"self\.stack\s*=\s*\[\]", content), "parser.py does not initialize self.stack in __init__"

    # Check that there isn't a class-level stack = [] right after class RPNParser:
    class_def = re.search(r"class\s+RPNParser\s*:(.*?)(?:def\s+__init__|def\s+parse_and_evaluate)", content, re.DOTALL)
    if class_def:
        assert "stack = []" not in class_def.group(1), "parser.py still has a class-level stack attribute"

def test_test_parser_implemented():
    with open("/home/user/math_project/tests/test_parser.py", "r") as f:
        content = f.read()

    assert "mock_open" in content, "test_parser.py does not use mock_open"
    assert "patch" in content, "test_parser.py does not use patch"
    assert "builtins.open" in content or "'open'" in content, "test_parser.py does not patch open"
    assert "20" in content, "test_parser.py does not assert the result is 20"
    assert "2 3 + 4 *" in content, "test_parser.py does not contain the mock file content '2 3 + 4 *'"

def test_run_tests_sh():
    script_path = "/home/user/run_tests.sh"
    assert os.path.isfile(script_path), "run_tests.sh is missing"

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), "run_tests.sh is not executable"

    with open(script_path, "r") as f:
        content = f.read()

    assert "cd /home/user/math_project" in content or "cd math_project" in content, "run_tests.sh does not change directory to math_project"
    assert "PYTHONPATH=src" in content, "run_tests.sh does not export PYTHONPATH=src"
    assert "python3 -m unittest discover -s tests" in content, "run_tests.sh does not run the tests correctly"
    assert ">" in content and "test_results.log" in content, "run_tests.sh does not redirect output to test_results.log"

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), "test_results.log is missing (did you run the script?)"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Ran 2 tests" in content, "test_results.log does not indicate that 2 tests ran"
    assert "OK" in content, "test_results.log does not indicate that tests passed (OK)"