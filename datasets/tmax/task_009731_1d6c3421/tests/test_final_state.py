# test_final_state.py

import os
import subprocess
import ast
import pytest

def test_c_file_fixed():
    """Verify that moving_average.c was updated to use malloc instead of a stack array."""
    path = "/home/user/migrator/moving_average.c"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "malloc" in content, "moving_average.c does not appear to use malloc for the return array."
    assert "float result[1000]" not in content, "moving_average.c still contains the buggy stack array 'float result[1000]'."

def test_python_migrated():
    """Verify that integration.py is valid Python 3 and no longer uses Python 2 print statements."""
    path = "/home/user/migrator/integration.py"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check if it parses as valid Python 3
    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"integration.py is not valid Python 3 syntax: {e}")

    # Extra check to ensure old print style is gone
    assert 'print "' not in content and "print '" not in content, "integration.py still contains Python 2 style print statements."

def test_go_test_created():
    """Verify that the Go unit test was created and contains the required test function."""
    path = "/home/user/migrator/main_test.go"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "TestComputeMA" in content, "main_test.go does not contain the function TestComputeMA."
    assert "computeMA" in content, "main_test.go does not appear to test the computeMA function."

def test_build_and_test_script():
    """Verify that build_and_test.sh runs successfully and produces the expected success.log."""
    script_path = "/home/user/migrator/build_and_test.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Remove success.log if it exists to ensure the script creates it
    log_path = "/home/user/migrator/success.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run the script
    result = subprocess.run(
        [script_path],
        cwd="/home/user/migrator",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"build_and_test.sh failed with exit code {result.returncode}.\n"
        f"Stdout:\n{result.stdout}\n"
        f"Stderr:\n{result.stderr}"
    )

    # Check that success.log was created and contains the exact string
    assert os.path.exists(log_path), f"{log_path} was not created by the script."

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    assert log_content == "ALL TESTS PASSED", f"success.log contains unexpected content: '{log_content}'"