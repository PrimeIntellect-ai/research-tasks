# test_final_state.py

import os
import re
import pytest

def test_anomalies_log_content():
    """Verify the presence and exact content of the anomalies.log file."""
    log_path = '/home/user/anomalies.log'
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_line = "Server: server_A, TS: 103, CPU: 40.00, MA: 21.00"

    # We check if the expected line is in the output (allowing for trailing newlines)
    assert expected_line in content, f"Expected log to contain '{expected_line}', but found:\n{content}"

def test_c_source_code_parameterized_queries():
    """Verify that the C source code uses parameterized queries."""
    src_path = '/home/user/analyze_metrics.c'
    assert os.path.exists(src_path), f"Source file {src_path} does not exist."

    with open(src_path, 'r') as f:
        src_content = f.read()

    assert 'sqlite3_prepare_v2' in src_content, "The C source code must use sqlite3_prepare_v2."
    assert 'sqlite3_bind_' in src_content, "The C source code must use sqlite3_bind_* functions."

def test_executable_exists():
    """Verify that the executable was compiled successfully."""
    exe_path = '/home/user/analyze_metrics'
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."