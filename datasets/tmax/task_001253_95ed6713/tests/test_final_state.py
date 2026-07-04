# test_final_state.py

import os
import json
import re
import pytest

def test_results_log_exists_and_correct():
    log_path = "/home/user/polymath/results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run test_run.py?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Log file {log_path} does not contain valid JSON. Content: {content}")

    assert "result" in data, "JSON response does not contain 'result' key"
    assert data["result"] == 20, f"Expected result to be 20, got {data['result']}"

def test_package_installed_with_node_api():
    try:
        import poly_calc
    except ImportError:
        pytest.fail("poly_calc package is not installed. Did you run 'pip install .' in python_client?")

    package_dir = os.path.dirname(poly_calc.__file__)
    node_api_dir = os.path.join(package_dir, "node_api")
    node_modules_dir = os.path.join(node_api_dir, "node_modules")
    server_js_path = os.path.join(node_api_dir, "server.js")

    assert os.path.isdir(node_api_dir), f"node_api directory not found in bundled package at {node_api_dir}"
    assert os.path.isdir(node_modules_dir), f"node_modules directory not found in bundled package at {node_modules_dir}. The build process should run npm install."
    assert os.path.isfile(server_js_path), f"server.js not found in bundled package at {server_js_path}"

def test_no_eval_in_server():
    server_js_path = "/home/user/polymath/node_api/server.js"
    assert os.path.isfile(server_js_path), f"File {server_js_path} does not exist"

    with open(server_js_path, "r") as f:
        content = f.read()

    assert not re.search(r'\beval\s*\(', content), "Usage of eval() is strictly forbidden in server.js"
    assert not re.search(r'\bFunction\s*\(', content), "Usage of Function constructor is strictly forbidden in server.js"

def test_test_run_script_exists():
    script_path = "/home/user/test_run.py"
    assert os.path.isfile(script_path), f"Test script {script_path} does not exist"