# test_final_state.py
import os
import sys
import subprocess
import pytest

APP_DIR = "/home/user/app"

def test_processor_fixed():
    """Check if processor.py has been fixed to raise ValueError on circular references."""
    if APP_DIR not in sys.path:
        sys.path.insert(0, APP_DIR)

    try:
        import processor
    except ImportError:
        pytest.fail("Could not import processor.py. Is it missing or broken?")

    # Reload to ensure we get the latest version if previously imported
    import importlib
    importlib.reload(processor)

    try:
        processor.flatten_data({"alias_of": "group_omega"})
        pytest.fail("flatten_data did not raise a ValueError on a circular reference.")
    except ValueError as e:
        assert "Circular reference detected" in str(e) or "circular" in str(e).lower(), \
            f"ValueError raised, but message was unexpected: {e}"
    except Exception as e:
        pytest.fail(f"flatten_data raised an unexpected exception: {e}")

def test_regression_file_contents():
    """Check if test_regression.py exists and contains the required elements."""
    test_file = os.path.join(APP_DIR, "test_regression.py")
    assert os.path.isfile(test_file), "test_regression.py is missing."

    with open(test_file, "r") as f:
        content = f.read()

    assert "unittest" in content, "test_regression.py does not use the unittest framework."
    assert "group_omega" in content, "test_regression.py does not contain the extracted alias 'group_omega'."
    assert "ValueError" in content, "test_regression.py does not assert that a ValueError is raised."
    assert "flatten_data" in content, "test_regression.py does not reference flatten_data."

def test_test_output_file():
    """Check if test_output.txt exists and indicates a successful test run."""
    output_file = os.path.join(APP_DIR, "test_output.txt")
    assert os.path.isfile(output_file), "test_output.txt is missing. Did you redirect the test output?"

    with open(output_file, "r") as f:
        content = f.read()

    assert "OK" in content, "test_output.txt does not contain 'OK', indicating the test may not have passed or output was not captured correctly."

def test_regression_execution():
    """Check if the regression test actually passes when run."""
    test_file = os.path.join(APP_DIR, "test_regression.py")
    assert os.path.isfile(test_file), "test_regression.py is missing."

    result = subprocess.run(
        [sys.executable, "-m", "unittest", test_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Running test_regression.py failed.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "OK" in result.stderr or "OK" in result.stdout, "Test execution did not output 'OK'."