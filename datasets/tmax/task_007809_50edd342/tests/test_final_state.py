# test_final_state.py

import os
import sys
import subprocess
import pytest
import importlib.util

SERVICE_DIR = "/home/user/service"
MATH_UTILS_PATH = os.path.join(SERVICE_DIR, "math_utils.py")
TEST_MATH_PATH = os.path.join(SERVICE_DIR, "test_math.py")
REQUIREMENTS_PATH = os.path.join(SERVICE_DIR, "requirements.txt")
RESOLUTION_LOG_PATH = "/home/user/resolution.log"

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def test_math_utils_logic():
    assert os.path.isfile(MATH_UTILS_PATH), f"{MATH_UTILS_PATH} does not exist."
    math_utils = load_module_from_path("math_utils", MATH_UTILS_PATH)

    assert hasattr(math_utils, "collatz_steps"), "collatz_steps function is missing."

    # Check valid case
    assert math_utils.collatz_steps(10) == 6, "collatz_steps(10) should return 6."

    # Check invalid case
    with pytest.raises(ValueError, match="positive"):
        math_utils.collatz_steps(0)
    with pytest.raises(ValueError):
        math_utils.collatz_steps(-5)

def test_regression_test_file():
    assert os.path.isfile(TEST_MATH_PATH), f"{TEST_MATH_PATH} does not exist."

    with open(TEST_MATH_PATH, 'r') as f:
        content = f.read()

    assert "test_collatz_valid" in content, "test_collatz_valid() is missing in test_math.py."
    assert "test_collatz_invalid" in content, "test_collatz_invalid() is missing in test_math.py."
    assert "pytest" in content or "ValueError" in content, "test_math.py doesn't seem to use pytest features properly."

    # Run pytest on the file
    result = subprocess.run([sys.executable, "-m", "pytest", TEST_MATH_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest failed on {TEST_MATH_PATH}:\n{result.stdout}\n{result.stderr}"

def test_requirements_updated():
    assert os.path.isfile(REQUIREMENTS_PATH), f"{REQUIREMENTS_PATH} does not exist."
    with open(REQUIREMENTS_PATH, 'r') as f:
        content = f.read().lower()

    # It should either have Werkzeug < 2.1.0 or Flask >= 2.2.0
    # We won't strictly parse versions, but we assume they changed it from the broken state.
    assert "werkzeug==2.2.2" not in content or "flask==2.0.1" not in content, "requirements.txt still contains the conflicting versions."

def test_resolution_log():
    assert os.path.isfile(RESOLUTION_LOG_PATH), f"{RESOLUTION_LOG_PATH} does not exist."
    with open(RESOLUTION_LOG_PATH, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"resolution.log must contain exactly two lines, found {len(lines)}."

    assert "flask" in lines[0].lower() or "werkzeug" in lines[0].lower(), "First line of resolution.log should mention Flask or Werkzeug."
    assert lines[1] == "TESTS_PASSED", "Second line of resolution.log must be 'TESTS_PASSED'."