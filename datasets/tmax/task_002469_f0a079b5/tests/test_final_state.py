# test_final_state.py

import os
import sys
import importlib.util

PROJECT_DIR = "/home/user/project"

def test_directory_structure_and_files():
    expected_files = [
        f"{PROJECT_DIR}/src/c_lib/math_ops.c",
        f"{PROJECT_DIR}/src/c_lib/libmath.so",
        f"{PROJECT_DIR}/src/pylib/interpreter.py",
        f"{PROJECT_DIR}/tests/test_interpreter.py",
        f"{PROJECT_DIR}/tests/test_config.py",
        f"{PROJECT_DIR}/tests/test_integration.py",
        f"{PROJECT_DIR}/test_results.log"
    ]

    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected file {file_path} is missing."

def test_no_leftovers_in_root():
    allowed_entries = {"src", "tests", "test_results.log"}
    actual_entries = set(os.listdir(PROJECT_DIR))

    # We allow some flexibility for pytest cache or pycache
    leftovers = [entry for entry in actual_entries if entry not in allowed_entries and not entry.startswith(".")]
    assert not leftovers, f"Found leftover files/directories in root: {leftovers}"

def test_ffi_dynamic_load_logic():
    interpreter_path = f"{PROJECT_DIR}/src/pylib/interpreter.py"
    with open(interpreter_path, "r") as f:
        content = f.read()

    # The requirement says it should resolve the path to ../c_lib/libmath.so relative to itself
    assert "os.path" in content or "Path" in content, "interpreter.py does not seem to dynamically resolve the path using os.path or pathlib."
    assert "c_lib" in content and "libmath.so" in content, "interpreter.py does not reference the relative path to libmath.so properly."

def test_circular_dependency_fixed():
    # We should be able to import interpreter.py without circular import errors
    interpreter_path = f"{PROJECT_DIR}/src/pylib/interpreter.py"

    spec = importlib.util.spec_from_file_location("interpreter", interpreter_path)
    interpreter = importlib.util.module_from_spec(spec)

    # Temporarily add paths so imports work if they rely on sys.path
    sys.path.insert(0, f"{PROJECT_DIR}/src/pylib")
    sys.path.insert(0, f"{PROJECT_DIR}/tests")

    try:
        spec.loader.exec_module(interpreter)
    except Exception as e:
        assert False, f"Importing interpreter.py failed, circular dependency might not be fixed. Error: {e}"
    finally:
        sys.path.pop(0)
        sys.path.pop(0)

def test_integration_test_contents():
    integration_test_path = f"{PROJECT_DIR}/tests/test_integration.py"
    with open(integration_test_path, "r") as f:
        content = f.read()

    assert "SUB 10 4" in content, "test_integration.py does not test 'SUB 10 4'."
    assert "6" in content, "test_integration.py does not assert the result is 6."

def test_test_results_log():
    log_path = f"{PROJECT_DIR}/test_results.log"
    with open(log_path, "r") as f:
        content = f.read()

    assert "passed" in content.lower(), "test_results.log does not indicate that tests passed."