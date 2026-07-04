# test_final_state.py

import os
import subprocess
import pytest
import ast

WORKSPACE = "/home/user/artifact_pipeline"

def test_makefile_fixed_and_binary_compiled():
    makefile_path = os.path.join(WORKSPACE, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}."

    # Run make to ensure it succeeds and builds the binary
    result = subprocess.run(["make", "-C", WORKSPACE], capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with output:\n{result.stdout}\n{result.stderr}"

    binary_path = os.path.join(WORKSPACE, "fletcher_calc")
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable."

def test_python_test_implementation():
    py_file = os.path.join(WORKSPACE, "test_fletcher.py")
    assert os.path.isfile(py_file), f"Python test file {py_file} does not exist."

    with open(py_file, "r") as f:
        content = f.read()

    assert "test_c_binary_matches_python" in content, "Test function `test_c_binary_matches_python` not found."
    assert "st.binary" in content, "Hypothesis strategy `st.binary` not used."
    assert "subprocess" in content, "subprocess module not used."

    # Parse the AST to verify the test function exists and has a decorator
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {py_file}: {e}")

    test_func_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "test_c_binary_matches_python":
            test_func_found = True
            # Check for @given decorator
            has_given = any(
                isinstance(d, ast.Call) and getattr(d.func, "id", "") == "given"
                for d in node.decorator_list
            )
            assert has_given, "`test_c_binary_matches_python` is missing the @given decorator."

    assert test_func_found, "Function `test_c_binary_matches_python` not found in AST."

def test_pytest_output_log():
    log_file = "/home/user/pytest_output.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    assert "passed" in content.lower(), f"Log file {log_file} does not indicate successful test execution."

def test_pipeline_status():
    status_file = "/home/user/pipeline_status.txt"
    assert os.path.isfile(status_file), f"Status file {status_file} does not exist."

    with open(status_file, "r") as f:
        content = f.read().strip()

    assert content == "PIPELINE_OK", f"Status file content is '{content}', expected 'PIPELINE_OK'."