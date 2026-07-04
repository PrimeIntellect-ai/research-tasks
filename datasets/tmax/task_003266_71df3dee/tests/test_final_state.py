# test_final_state.py

import os
import subprocess
import pytest

def test_mre_txt_contains_correct_value():
    mre_path = "/home/user/project/mre.txt"
    assert os.path.isfile(mre_path), f"{mre_path} is missing. You must create it."

    with open(mre_path, "r") as f:
        content = f.read().strip()

    # The failing input based on the log is 16.0
    assert "16.0" in content, f"{mre_path} does not contain the correct failing input value. Check the build.log timeline carefully."

def test_generator_c_is_fixed():
    generator_path = "/home/user/project/src/generator.c"
    assert os.path.isfile(generator_path), f"{generator_path} is missing."

    with open(generator_path, "r") as f:
        content = f.read()

    # The original bug was `double df = 2.0;`
    # The fix should involve multiplying by x, so `double df = 2.0;` should be gone.
    assert "double df = 2.0;" not in content, "The bug in src/generator.c has not been fixed. The derivative of x^2 - n is 2x, not 2."

def test_app_compiles_and_runs():
    app_path = "/home/user/project/app"
    assert os.path.isfile(app_path), f"The compiled binary {app_path} is missing. Did you run 'make'?"
    assert os.access(app_path, os.X_OK), f"{app_path} is not executable."

    try:
        result = subprocess.run([app_path], capture_output=True, text=True, timeout=2)
        assert result.returncode == 0, f"Running {app_path} failed with return code {result.returncode}."
        assert "Application initialized successfully." in result.stdout, f"Unexpected output from {app_path}: {result.stdout}"
    except subprocess.TimeoutExpired:
        pytest.fail(f"Running {app_path} timed out. There might be an infinite loop in the generator or app.")
    except Exception as e:
        pytest.fail(f"Failed to run {app_path}: {e}")