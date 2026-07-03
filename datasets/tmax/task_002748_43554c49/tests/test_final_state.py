# test_final_state.py

import os
import subprocess
import re
import pytest

def test_report_exists_and_correct():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_log = "Faulty Log: log_073.bin"
    expected_bytes = "Leaked Bytes per request: 25"

    assert expected_log in content, f"Report does not correctly identify the faulty log. Expected '{expected_log}'."
    assert expected_bytes in content, f"Report does not correctly identify the leaked bytes. Expected '{expected_bytes}'."

def test_parser_h_fixed():
    parser_path = "/home/user/telemetryd/parser.h"
    assert os.path.isfile(parser_path), f"{parser_path} is missing."

    with open(parser_path, "r") as f:
        content = f.read()

    assert "<stdint.h>" in content, "parser.h is still missing the #include <stdint.h> directive."

def test_makefile_fixed():
    makefile_path = "/home/user/telemetryd/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-pthread" in content, "Makefile is still missing the -pthread flag required for compilation."

def test_telemetryd_compiles():
    # Clean first
    subprocess.run(["make", "clean"], cwd="/home/user/telemetryd", capture_output=True)

    # Run make
    result = subprocess.run(["make"], cwd="/home/user/telemetryd", capture_output=True, text=True)
    assert result.returncode == 0, f"Compilation failed after fixes:\n{result.stderr}"

    exe_path = "/home/user/telemetryd/telemetryd"
    assert os.path.isfile(exe_path), f"Executable {exe_path} was not created by make."
    assert os.access(exe_path, os.X_OK), f"Executable {exe_path} is not executable."

def test_server_c_memory_leak_fixed():
    server_path = "/home/user/telemetryd/server.c"
    assert os.path.isfile(server_path), f"{server_path} is missing."

    with open(server_path, "r") as f:
        content = f.read()

    # We look for the bounds check block: if (offset + 1 + item_len > total_len)
    # Inside this block, there should be a free(item) before the break.

    bounds_check_pattern = re.compile(r"if\s*\([^)]*>\s*total_len\s*\)\s*\{([^}]*)\}")
    match = bounds_check_pattern.search(content)

    assert match is not None, "Could not find the bounds check logic in server.c"

    block_content = match.group(1)
    assert "free" in block_content and "item" in block_content, "The memory leak is not fixed. Missing free(item) in the out-of-bounds error handling block."