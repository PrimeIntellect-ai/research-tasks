# test_final_state.py

import os
import json
import urllib.request
import urllib.error

def test_result_json():
    """Verify the contents of /home/user/project/result.json"""
    json_path = "/home/user/project/result.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not valid JSON."

    assert "symbol_name" in data, "Key 'symbol_name' missing in result.json"
    assert "computation_result" in data, "Key 'computation_result' missing in result.json"

    assert data["symbol_name"] == "sys_asm_calc_expr_v2", f"Expected symbol_name 'sys_asm_calc_expr_v2', got '{data['symbol_name']}'"
    assert data["computation_result"] == 36, f"Expected computation_result 36, got {data['computation_result']}"

def test_nginx_reverse_proxy():
    """Verify that Nginx is reverse proxying port 8080 to the Python server on port 9000."""
    url = "http://127.0.0.1:8080/"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()

            assert status == 200, f"Expected HTTP 200, got {status}"
            assert body == "36", f"Expected response body '36', got '{body}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx on {url}: {e}"

def test_python_server_direct():
    """Verify that the Python server is running directly on port 9000."""
    url = "http://127.0.0.1:9000/"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()

            assert status == 200, f"Expected HTTP 200, got {status}"
            assert body == "36", f"Expected response body '36', got '{body}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Python server on {url}: {e}"

def test_scripts_exist():
    """Verify that the required Python scripts were created."""
    assert os.path.isfile("/home/user/project/parser.py"), "/home/user/project/parser.py is missing"
    assert os.path.isfile("/home/user/project/server.py"), "/home/user/project/server.py is missing"