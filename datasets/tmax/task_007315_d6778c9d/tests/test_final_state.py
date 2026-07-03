# test_final_state.py

import os
import subprocess
import pytest

def test_recovered_log_exists_and_content():
    path = "/home/user/recovered_log.txt"
    assert os.path.isfile(path), f"Recovered log file {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    assert "[INFO] User login successful" in content, "Recovered log is missing the INFO line."
    assert "[ERROR] Failed to load \"config.json\" - retrying" in content, "Recovered log is missing the ERROR line."
    assert "[WARN] Empty" in content, "Recovered log is missing the WARN line."

def test_filter_tool_compiled():
    path = "/home/user/filter_tool"
    assert os.path.isfile(path), f"Compiled tool {path} is missing."
    assert os.access(path, os.X_OK), f"Compiled tool {path} is not executable."

def test_build_tool_fixed():
    path = "/home/user/build_tool.sh"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "-lm" in content, "build_tool.sh does not contain '-lm' to link the math library."

def test_process_logs_fixed():
    path = "/home/user/process_logs.sh"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()

    # The infinite loop should be fixed (e.g., break instead of continue)
    # We check that 'continue' in the EOF block is gone or replaced by 'break' or 'exit'
    # Since the student might have rewritten the loop, we just verify the output is correct, 
    # but we can also check for quotes around $msg
    assert '"$msg"' in content or "${msg}" in content or "”$msg”" in content or "score=$(./filter_tool \"$msg\")" in content, "process_logs.sh does not seem to quote the $msg variable."

def test_final_output_correct():
    path = "/home/user/final_output.txt"
    assert os.path.isfile(path), f"Final output file {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()

    expected = "Error score: 6.32"
    assert content == expected, f"Expected '{expected}', got '{content}'"