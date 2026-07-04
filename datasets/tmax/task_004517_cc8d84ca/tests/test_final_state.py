# test_final_state.py

import os
import subprocess
import ast

PROJECT_DIR = "/home/user/project"
REPORT_FILE = "/home/user/report.txt"

def test_project_structure():
    """Verify the project has been reorganized correctly."""
    src_dir = os.path.join(PROJECT_DIR, "src")
    app_dir = os.path.join(src_dir, "app")
    tests_dir = os.path.join(PROJECT_DIR, "tests")

    assert os.path.isdir(src_dir), f"Directory {src_dir} does not exist."
    assert os.path.isdir(app_dir), f"Directory {app_dir} does not exist."
    assert os.path.isdir(tests_dir), f"Directory {tests_dir} does not exist."

    assert os.path.isfile(os.path.join(src_dir, "__init__.py")), "src/__init__.py is missing."
    assert os.path.isfile(os.path.join(app_dir, "__init__.py")), "src/app/__init__.py is missing."
    assert os.path.isfile(os.path.join(tests_dir, "__init__.py")), "tests/__init__.py is missing."

    for file in ["main.py", "router.py", "utils.py"]:
        app_file = os.path.join(app_dir, file)
        root_file = os.path.join(PROJECT_DIR, file)
        assert os.path.isfile(app_file), f"{file} was not moved to {app_dir}."
        assert not os.path.exists(root_file), f"{file} still exists in the root directory."

def test_report_file():
    """Verify the report file content."""
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."
    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Report file should contain exactly 2 lines, found {len(lines)}."
    assert lines[0] == "/home/user/project/src/app/router.py", f"Line 1 is incorrect: {lines[0]}"
    assert lines[1] == "_route_cache", f"Line 2 is incorrect: {lines[1]}"

def test_router_memory_leak_fix():
    """Verify the memory leak was fixed using lru_cache."""
    router_path = os.path.join(PROJECT_DIR, "src", "app", "router.py")
    assert os.path.isfile(router_path), f"File {router_path} does not exist."

    with open(router_path, "r") as f:
        content = f.read()

    assert "_route_cache" not in content, "The global dictionary '_route_cache' must be removed."

    # Parse AST to check for lru_cache decorator
    tree = ast.parse(content)
    has_lru_cache = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "parse_url":
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    if getattr(decorator.func, "id", "") == "lru_cache" or getattr(decorator.func, "attr", "") == "lru_cache":
                        for kw in decorator.keywords:
                            if kw.arg == "maxsize" and isinstance(kw.value, ast.Constant) and kw.value.value == 128:
                                has_lru_cache = True

    assert has_lru_cache, "parse_url must be decorated with @lru_cache(maxsize=128)."

def test_test_suite_execution():
    """Verify the student's test suite runs successfully."""
    test_file = os.path.join(PROJECT_DIR, "tests", "test_router.py")
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."

    # Run the tests
    result = subprocess.run(
        ["python3", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Tests failed to run successfully:\n{result.stderr}\n{result.stdout}"