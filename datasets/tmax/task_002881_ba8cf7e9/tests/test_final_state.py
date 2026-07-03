# test_final_state.py

import os
import subprocess
import ast

def test_suspicious_py_exists():
    assert os.path.isfile('/home/user/recovered/suspicious.py'), "/home/user/recovered/suspicious.py is missing"

def test_test_suspicious_py_exists():
    assert os.path.isfile('/home/user/recovered/test_suspicious.py'), "/home/user/recovered/test_suspicious.py is missing"

def test_suspicious_py_fixed():
    with open('/home/user/recovered/suspicious.py', 'r') as f:
        content = f.read()

    # Parse the AST to check the lock acquisition order in release_connection
    tree = ast.parse(content)

    release_func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'release_connection':
            release_func = node
            break

    assert release_func is not None, "Function release_connection not found in suspicious.py"

    # We expect 'with self.conn_lock' to be the outer with, and 'with self.state_lock' to be the inner.
    # We can just check the source code text to be simple, or do a basic string check.
    # In the original, release_connection has:
    # with self.state_lock:
    #     time.sleep(0.01)
    #     with self.conn_lock:
    # The fix should acquire conn_lock first.

    # Let's just run the module and see if it deadlocks. If it doesn't deadlock, the fix is likely correct.
    # But wait, we can also just check that "conn_lock" appears before "state_lock" in the release_connection body.
    body_text = ast.get_source_segment(content, release_func)
    conn_idx = body_text.find('conn_lock')
    state_idx = body_text.find('state_lock')

    assert conn_idx != -1 and state_idx != -1, "Locks not found in release_connection"
    assert conn_idx < state_idx, "conn_lock must be acquired before state_lock in release_connection to fix the deadlock"

def test_pytest_runs_successfully():
    # Run the student's pytest file
    result = subprocess.run(
        ['pytest', '/home/user/recovered/test_suspicious.py'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest failed with output:\n{result.stdout}\n{result.stderr}"

def test_test_suspicious_py_timeout_configured():
    with open('/home/user/recovered/test_suspicious.py', 'r') as f:
        content = f.read()

    assert 'timeout' in content, "The test file does not seem to configure a timeout. Use pytest-timeout."
    assert 'run' in content, "The test file does not import or use the 'run' function."