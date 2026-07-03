# test_final_state.py

import os
import re
import pytest

def test_build_rs_fixed():
    build_rs_path = "/home/user/data_pipeline/build.rs"
    assert os.path.isfile(build_rs_path), f"File {build_rs_path} is missing."

    with open(build_rs_path, "r") as f:
        content = f.read()

    assert ".cpp(true)" in content, "build.rs is not fixed: missing .cpp(true) to compile as C++."

def test_processor_cpp_fixed():
    processor_cpp_path = "/home/user/data_pipeline/cpp_src/processor.cpp"
    assert os.path.isfile(processor_cpp_path), f"File {processor_cpp_path} is missing."

    with open(processor_cpp_path, "r") as f:
        content = f.read()

    assert "i <= len" not in content, "processor.cpp still contains the off-by-one bug (i <= len)."

    # Check for a valid loop condition like i < len
    assert re.search(r"i\s*<\s*len", content) or re.search(r"i\s*!=\s*len", content), \
        "processor.cpp does not appear to have a corrected loop condition (e.g. i < len)."

def test_result_log():
    result_log_path = "/home/user/result.log"
    assert os.path.isfile(result_log_path), f"Result log file {result_log_path} was not created."

    with open(result_log_path, "r") as f:
        content = f.read().strip()

    assert "Result: 61" in content, f"Expected 'Result: 61' in {result_log_path}, found: '{content}'"