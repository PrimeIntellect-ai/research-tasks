# test_final_state.py

import os
import stat
import pytest

BASE_DIR = "/home/user/ci_pipeline"

def test_makefile_fixed():
    makefile_path = os.path.join(BASE_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing."

    with open(makefile_path, 'r') as f:
        makefile_content = f.read()

    # Check that expr_parser.o is used in the linking step
    # The original was: $(CXX) $(CXXFLAGS) -o evaluator main.o
    # It should now be: $(CXX) $(CXXFLAGS) -o evaluator main.o expr_parser.o (or similar)
    # We can check if 'expr_parser.o' appears on the same line as '-o evaluator'
    lines = makefile_content.splitlines()
    linking_line_found = False
    for line in lines:
        if "-o evaluator" in line and "main.o" in line and "expr_parser.o" in line:
            linking_line_found = True
            break

    assert linking_line_found, "Makefile linking step is not fixed. It should include expr_parser.o when building the evaluator executable."

def test_expr_parser_fixed():
    cpp_path = os.path.join(BASE_DIR, "expr_parser.cpp")
    assert os.path.isfile(cpp_path), f"{cpp_path} is missing."

    with open(cpp_path, 'r') as f:
        cpp_content = f.read()

    assert "return left - right;" in cpp_content, "The subtraction bug in expr_parser.cpp is not fixed. It should return 'left - right'."
    assert "return right - left;" not in cpp_content, "The original subtraction bug is still present in expr_parser.cpp."

def test_binary_built():
    binary_path = os.path.join(BASE_DIR, "evaluator")
    assert os.path.isfile(binary_path), f"The evaluator binary was not built at {binary_path}."

    # Check if executable
    st = os.stat(binary_path)
    assert st.st_mode & stat.S_IXUSR, f"The evaluator file at {binary_path} is not executable."

def test_test_results_log():
    log_path = os.path.join(BASE_DIR, "test_results.log")
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, 'r') as f:
        log_content = f.read().strip()

    assert "ALL TESTS PASSED" in log_content, f"test_results.log does not contain 'ALL TESTS PASSED'. Content found: {log_content}"