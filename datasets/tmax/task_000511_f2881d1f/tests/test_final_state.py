# test_final_state.py

import os
import re

def test_shared_library_compiled():
    so_path = "/home/user/python_processor/libdataparser.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} does not exist. Did you compile and copy it?"
    # Check if it's an ELF file
    with open(so_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{so_path} is not a valid ELF shared library."

def test_wrapper_abi_fixed():
    wrapper_path = "/home/user/python_processor/wrapper.py"
    assert os.path.isfile(wrapper_path), f"File {wrapper_path} does not exist."
    with open(wrapper_path, "r") as f:
        content = f.read()

    # Check for correct types
    assert "ctypes.c_double" in content, "wrapper.py must use ctypes.c_double for f64."
    assert "ctypes.c_size_t" in content, "wrapper.py must use ctypes.c_size_t for usize."
    assert "ctypes.c_float" not in content, "wrapper.py should not contain ctypes.c_float."
    assert "ctypes.c_int" not in content, "wrapper.py should not contain ctypes.c_int."

def test_pytest_file_exists_and_contains_requirements():
    test_file = "/home/user/python_processor/tests/test_processor.py"
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."
    with open(test_file, "r") as f:
        content = f.read()

    assert "def test_process_and_report" in content, "Test function 'test_process_and_report' is missing."
    assert "150.0" in content, "The test should assert the sum is 150.0."
    assert "patch" in content or "mocker" in content, "The test must use patch or mocker to mock report_analytics."

def test_pytest_log_exists_and_passed():
    log_file = "/home/user/test_results.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist. Did you run the pytest command and redirect output?"

    with open(log_file, "r") as f:
        content = f.read()

    assert re.search(r"1 passed", content) or re.search(r"passed.*1", content), "The pytest log does not indicate that 1 test passed."
    assert "FAILED" not in content, "The pytest log contains failures."