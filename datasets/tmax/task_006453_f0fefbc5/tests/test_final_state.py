# test_final_state.py

import os
import re

def test_sandbox_c_exists():
    assert os.path.isfile('/home/user/sandbox.c'), "/home/user/sandbox.c is missing"

def test_sandbox_compiled_and_executable():
    assert os.path.isfile('/home/user/sandbox'), "/home/user/sandbox is missing"
    assert os.access('/home/user/sandbox', os.X_OK), "/home/user/sandbox is not executable"

def test_sandbox_c_logic():
    with open('/home/user/sandbox.c', 'r') as f:
        content = f.read()

    assert 'fork' in content, "sandbox.c does not contain a call to fork()"
    assert 'setrlimit' in content, "sandbox.c does not contain a call to setrlimit()"
    assert 'RLIMIT_FSIZE' in content, "sandbox.c does not reference RLIMIT_FSIZE"
    assert re.search(r'wait|waitpid', content), "sandbox.c does not contain a call to wait() or waitpid()"

    assert 'VULNERABLE: SIGNAL' in content, "sandbox.c does not contain the required string 'VULNERABLE: SIGNAL'"
    assert 'SECURE: EXIT' in content, "sandbox.c does not contain the required string 'SECURE: EXIT'"

def test_final_report_content():
    report_path = '/home/user/final_report.txt'
    assert os.path.isfile(report_path), f"{report_path} is missing"

    with open(report_path, 'r') as f:
        content = f.read().strip()

    assert content == 'VULNERABLE: SIGNAL 11', f"final_report.txt contains incorrect output: expected 'VULNERABLE: SIGNAL 11', got '{content}'"