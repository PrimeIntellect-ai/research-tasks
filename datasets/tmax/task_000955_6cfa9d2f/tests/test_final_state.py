# test_final_state.py

import os
import json
import pytest
import ast

def test_result_log_exists_and_valid():
    """Test that result.log exists and contains the expected JSON structure."""
    log_path = '/home/user/result.log'
    assert os.path.isfile(log_path), f"{log_path} is missing. Did you redirect the output of client.py?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content, f"{log_path} is empty."

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"{log_path} does not contain valid JSON.")

    assert "status_code" in data, "JSON in result.log is missing 'status_code'."
    assert data["status_code"] == 200, f"Expected status_code 200, got {data['status_code']}."

    assert "headers" in data, "JSON in result.log is missing 'headers'."
    headers = {k.lower(): v for k, v in data["headers"].items()}

    expected_csp = "default-src 'none'; frame-ancestors 'none';"
    assert "content-security-policy" in headers, "Content-Security-Policy header is missing in the response."
    assert headers["content-security-policy"] == expected_csp, f"Expected CSP '{expected_csp}', got '{headers['content-security-policy']}'."

def test_server_py_rotated_certs():
    """Test that server.py uses the new certificates."""
    server_path = '/home/user/app/server.py'
    assert os.path.isfile(server_path), f"{server_path} is missing."

    with open(server_path, 'r') as f:
        content = f.read()

    assert 'new_server.crt' in content, "server.py does not appear to use new_server.crt."
    assert 'new_server.key' in content, "server.py does not appear to use new_server.key."
    assert 'old_server.crt' not in content, "server.py is still referencing old_server.crt."
    assert 'old_server.key' not in content, "server.py is still referencing old_server.key."

def test_client_py_validates_chain():
    """Test that client.py uses the new CA bundle to verify the server certificate."""
    client_path = '/home/user/app/client.py'
    assert os.path.isfile(client_path), f"{client_path} is missing."

    with open(client_path, 'r') as f:
        content = f.read()

    assert 'verify=False' not in content.replace(' ', ''), "client.py is still using verify=False."
    assert 'new_ca.pem' in content, "client.py does not appear to use new_ca.pem for verification."

    # Parse AST to be more robust
    try:
        tree = ast.parse(content)
    except SyntaxError:
        pytest.fail("client.py contains invalid Python syntax.")

    found_verify = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr in ('get', 'post', 'request'):
                for kw in node.keywords:
                    if kw.arg == 'verify':
                        if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                            if 'new_ca.pem' in kw.value.value:
                                found_verify = True
                        elif isinstance(kw.value, ast.Str): # Python < 3.8
                            if 'new_ca.pem' in kw.value.s:
                                found_verify = True

    assert found_verify, "client.py does not pass the correct CA bundle path to the requests call."