# test_final_state.py
import os
import subprocess
import pytest

def test_result_log():
    log_path = '/home/user/result.log'
    assert os.path.isfile(log_path), f"File {log_path} does not exist. The task requires saving the result to this file."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == '21', f"Expected /home/user/result.log to contain exactly '21', but got '{content}'."

def test_expr_app_exists_and_executable():
    app_path = '/home/user/expr_project/expr_app'
    assert os.path.isfile(app_path), f"Executable {app_path} does not exist. Ensure the build script compiles to this location."
    assert os.access(app_path, os.X_OK), f"File {app_path} is not executable."

def test_bounds_checking_via_expr_app():
    app_path = '/home/user/expr_project/expr_app'
    if not os.path.isfile(app_path):
        pytest.fail(f"Executable {app_path} not found, cannot test bounds checking.")

    # Run the app with an expression that overflows the stack (size 4)
    # Pushing 5 elements: 1, 2, 3, 4, 5
    result = subprocess.run([app_path, "1 2 3 4 5 + + + +"], capture_output=True, text=True)
    output = result.stdout.strip()

    assert output == '-999', (
        f"Expected bounds check to return '-999' when stack size exceeds 4, "
        f"but got '{output}'. Ensure eval.c returns -999 if sp >= 4 during a push."
    )

def test_valid_expression_evaluation():
    app_path = '/home/user/expr_project/expr_app'
    if not os.path.isfile(app_path):
        pytest.fail(f"Executable {app_path} not found, cannot test evaluation.")

    # Run the app with the valid expression from the prompt
    result = subprocess.run([app_path, "10 5 2 * + 8 4 / - 3 +"], capture_output=True, text=True)
    output = result.stdout.strip()

    assert output == '21', f"Expected valid expression to evaluate to '21', but got '{output}'."