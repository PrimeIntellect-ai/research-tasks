# test_final_state.py

import os
import ast

def test_shared_library_exists():
    """Test that the compiled Go shared library exists."""
    so_file = "/home/user/libmatheval.so"
    assert os.path.isfile(so_file), f"Expected shared library {so_file} is missing. Did you compile the Go code?"

def test_integration_script_exists_and_valid():
    """Test that the Python integration script exists and imports ctypes."""
    py_file = "/home/user/test_integration.py"
    assert os.path.isfile(py_file), f"Expected Python script {py_file} is missing."

    with open(py_file, "r") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        assert False, f"Python script {py_file} contains a syntax error: {e}"

    imports_ctypes = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "ctypes":
                    imports_ctypes = True
        elif isinstance(node, ast.ImportFrom):
            if node.module == "ctypes":
                imports_ctypes = True

    assert imports_ctypes, f"Python script {py_file} does not import 'ctypes'."

def test_math_output():
    """Test that the output file exists and contains the correct result."""
    out_file = "/home/user/math_output.txt"
    assert os.path.isfile(out_file), f"Expected output file {out_file} is missing. Did you run your Python script?"

    with open(out_file, "r") as f:
        content = f.read().strip()

    assert content == "14.0", f"Expected output to be '14.0', but got '{content}'."