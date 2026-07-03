# test_final_state.py

import os
import subprocess
import ast

def test_migration_result_exists_and_correct():
    result_path = '/home/user/token_gen/migration_result.txt'
    assert os.path.isfile(result_path), f"The file {result_path} does not exist. Did you save the output?"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_line1 = "Generating token for user: test_user_123"
    expected_line2 = "Generated: TOKEN-667709-SEC"

    assert expected_line1 in content, f"Expected '{expected_line1}' to be in migration_result.txt"
    assert expected_line2 in content, f"Expected '{expected_line2}' to be in migration_result.txt. Ensure the secure build was used and the C logic is correct."

def test_python_wrapper_is_python3():
    py_path = '/home/user/token_gen/wrapper.py'
    assert os.path.isfile(py_path), f"The file {py_path} is missing."

    with open(py_path, 'r') as f:
        source = f.read()

    try:
        ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"wrapper.py is not valid Python 3 syntax: {e}")

def test_makefile_has_secure_target():
    makefile_path = '/home/user/token_gen/Makefile'
    assert os.path.isfile(makefile_path), f"The file {makefile_path} is missing."

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert 'secure:' in content, "The Makefile is missing the 'secure' target."
    assert 'SECURE_MODE' in content, "The Makefile secure target does not seem to define SECURE_MODE."

def test_token_bin_is_executable():
    bin_path = '/home/user/token_gen/token_bin'
    assert os.path.isfile(bin_path), f"The compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"The file {bin_path} is not executable."