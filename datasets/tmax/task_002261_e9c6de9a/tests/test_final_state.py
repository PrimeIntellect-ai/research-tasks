# test_final_state.py
import os
import py_compile
import importlib.metadata
import pytest

def test_setup_py_compiles():
    """Verify that setup.py no longer has a syntax error."""
    setup_path = '/home/user/app/setup.py'
    assert os.path.exists(setup_path), f"{setup_path} is missing."
    try:
        py_compile.compile(setup_path, doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"setup.py still has a syntax error: {e}")

def test_package_installed():
    """Verify that the logparser package is installed."""
    try:
        importlib.metadata.version('logparser')
    except importlib.metadata.PackageNotFoundError:
        pytest.fail("Package 'logparser' is not installed. Did you run pip install -e /home/user/app?")

def test_failures_log_exists_and_correct():
    """Verify that the parser caught the struct.error and wrote to failures.txt correctly."""
    failures_file = '/home/user/failures.txt'
    assert os.path.exists(failures_file), f"{failures_file} does not exist. Did the script run and catch the error?"

    with open(failures_file, 'r') as f:
        content = f.read().strip()

    expected_string = "MALFORMED_RECORD_AT_OFFSET_8"
    assert expected_string in content, f"Expected to find '{expected_string}' in {failures_file}, but got:\n{content}"