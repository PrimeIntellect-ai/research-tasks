# test_final_state.py

import os
import re
import pytest

def test_leak_report_content():
    report_path = "/home/user/leak_report.txt"
    assert os.path.isfile(report_path), f"File not found: {report_path}"

    with open(report_path, 'r') as f:
        content = f.read().strip()

    assert content == "83920", f"leak_report.txt does not contain the correct leaked session ID. Found: '{content}'"

def test_session_manager_cpp_fixed():
    cpp_path = "/home/user/session_manager.cpp"
    assert os.path.isfile(cpp_path), f"File not found: {cpp_path}"

    with open(cpp_path, 'r') as f:
        content = f.read()

    assert "delete" in content, "session_manager.cpp does not contain a 'delete' statement."

    # Extract the handle_disconnect function body roughly
    func_match = re.search(r'void\s+handle_disconnect\s*\([^)]*\)\s*\{(.*?)\n\}', content, re.DOTALL)
    assert func_match, "Could not find 'handle_disconnect' function body."
    func_body = func_match.group(1)

    # Check if delete is in the else block or used unconditionally
    # The original buggy code had:
    # if (graceful) { delete s; } else { ... }

    # Find the else block
    else_match = re.search(r'else\s*\{([^}]+)\}', func_body, re.DOTALL)
    if else_match:
        else_body = else_match.group(1)
        assert "delete " in else_body, "The 'delete' statement was not found in the 'else' block for non-graceful disconnects."
    else:
        # If they refactored to remove the if/else and just delete unconditionally
        assert "delete " in func_body, "The 'delete' statement was not found in the 'handle_disconnect' function."