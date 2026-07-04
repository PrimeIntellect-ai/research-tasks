# test_final_state.py
import os
import ast
import pytest

def test_payload_txt():
    path = '/home/user/payload.txt'
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    expected = 'metric=DISK|val=NaN_ERROR_99'
    assert content == expected, f"payload.txt contains '{content}' instead of the expected payload '{expected}'."

def test_server_py_patched():
    path = '/home/user/monitor_service/server.py'
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, 'r') as f:
        code = f.read()

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        pytest.fail(f"server.py has a syntax error: {e}")

    safe_lock = False
    for node in ast.walk(tree):
        # Check for 'with lock:'
        if isinstance(node, ast.With):
            for item in node.items:
                if isinstance(item.context_expr, ast.Name) and item.context_expr.id == 'lock':
                    safe_lock = True
        # Check for 'try...finally' containing 'lock.release()'
        elif isinstance(node, ast.Try):
            for stmt in node.finalbody:
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                    func = stmt.value.func
                    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                        if func.value.id == 'lock' and func.attr == 'release':
                            safe_lock = True

    assert safe_lock, "server.py does not safely release the lock. You must use a 'with lock:' context manager or a 'try...finally' block calling 'lock.release()'."

def test_mre_py_exists_and_correct():
    path = '/home/user/mre.py'
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    expected_payload = 'metric=DISK|val=NaN_ERROR_99'
    assert expected_payload in content, f"mre.py does not contain the malicious payload: {expected_payload}"
    assert 'socket' in content or 'UDP' in content or 'scapy' in content, "mre.py does not appear to contain network code to send the payload."