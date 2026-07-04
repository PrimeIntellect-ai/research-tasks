# test_final_state.py

import os
import re
import pytest

def test_cmakelists_linked():
    cmakelists_path = "/home/user/project/CMakeLists.txt"
    assert os.path.isfile(cmakelists_path), f"File {cmakelists_path} is missing."

    with open(cmakelists_path, "r") as f:
        content = f.read()

    # Check if target_link_libraries is used to link test_app and math_lib
    # It might be target_link_libraries(test_app math_lib) or similar
    match = re.search(r"target_link_libraries\s*\(\s*test_app\s+(?:PRIVATE\s+|PUBLIC\s+|INTERFACE\s+)?math_lib\s*\)", content)
    assert match is not None, "CMakeLists.txt does not correctly link test_app against math_lib using target_link_libraries."

def test_math_lib_cpp_fixed():
    math_lib_cpp_path = "/home/user/project/src/math_lib.cpp"
    assert os.path.isfile(math_lib_cpp_path), f"File {math_lib_cpp_path} is missing."

    with open(math_lib_cpp_path, "r") as f:
        content = f.read()

    # The original bug was `i <= v.size()`. Ensure it is fixed.
    assert "i <= v.size()" not in content, "The out-of-bounds bug 'i <= v.size()' is still present in math_lib.cpp."

    # Check for a valid loop condition like i < v.size() or i != v.size()
    assert re.search(r"i\s*<\s*v\.size\(\)", content) or re.search(r"i\s*!=\s*v\.size\(\)", content), \
        "math_lib.cpp does not seem to contain a corrected loop boundary (e.g., i < v.size())."

def test_test_result_log():
    log_path = "/home/user/project/test_result.log"
    assert os.path.isfile(log_path), f"The test result log file {log_path} was not created. Did you compile and run the test_app?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "PROPERTY_TEST_PASSED", f"Expected the log file to contain exactly 'PROPERTY_TEST_PASSED', but found '{content}'."

def test_test_app_cpp_modified():
    test_app_cpp_path = "/home/user/project/test/test_app.cpp"
    assert os.path.isfile(test_app_cpp_path), f"File {test_app_cpp_path} is missing."

    with open(test_app_cpp_path, "r") as f:
        content = f.read()

    # Check that the file has been modified to include some property test logic
    assert "100" in content, "test_app.cpp does not seem to contain the logic for 100 random vectors."
    assert "PROPERTY_TEST_PASSED" in content, "test_app.cpp does not contain the success string to write to the log."
    assert "PROPERTY_TEST_FAILED" in content, "test_app.cpp does not contain the failure string to write to the log."
    assert "test_result.log" in content, "test_app.cpp does not contain the filename 'test_result.log' to write to."