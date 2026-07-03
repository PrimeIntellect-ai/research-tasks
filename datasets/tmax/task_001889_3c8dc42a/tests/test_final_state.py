# test_final_state.py

import json
import subprocess
import os

def test_load_test_metrics():
    """
    Executes the load test script and asserts that throughput and memory
    growth meet the required thresholds.
    """
    load_test_script = "/home/user/app/load_test.py"
    assert os.path.exists(load_test_script), f"Load test script missing: {load_test_script}"

    try:
        output = subprocess.check_output(['python3', load_test_script], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        assert False, f"Load test script failed to execute. Output:\n{e.output.decode('utf-8')}"

    try:
        # Attempt to parse the JSON output
        # Find the first '{' and last '}' in case there's extra logging
        start_idx = output.find('{')
        end_idx = output.rfind('}') + 1
        assert start_idx != -1 and end_idx != 0, "No JSON object found in load test output."

        json_str = output[start_idx:end_idx]
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        assert False, f"Failed to parse JSON from load test output. Output was:\n{output}\nError: {e}"

    assert 'requests_per_second' in data, "JSON output missing 'requests_per_second' key."
    assert 'memory_growth_mb' in data, "JSON output missing 'memory_growth_mb' key."

    throughput = data['requests_per_second']
    memory_growth_mb = data['memory_growth_mb']

    assert throughput >= 500.0, f"Throughput too low: {throughput} req/s (expected >= 500.0 req/s)"
    assert memory_growth_mb < 5.0, f"Memory growth too high: {memory_growth_mb} MB (expected < 5.0 MB)"

def test_nginx_config_proxy_pass():
    """
    Verifies that the Nginx configuration has been updated to proxy requests to the Flask app.
    """
    nginx_conf_path = "/home/user/app/nginx.conf"
    assert os.path.exists(nginx_conf_path), f"Nginx configuration missing: {nginx_conf_path}"

    with open(nginx_conf_path, 'r') as f:
        content = f.read()

    # Check for proxy_pass directive pointing to port 5000
    has_proxy_pass = "proxy_pass http://127.0.0.1:5000" in content or "proxy_pass http://localhost:5000" in content
    assert has_proxy_pass, "Nginx configuration is missing the 'proxy_pass' directive to http://127.0.0.1:5000"

def test_api_tests_pass():
    """
    Verifies that the test fixtures have been fixed and tests pass successfully.
    """
    test_file = "/home/user/app/tests/test_api.py"
    assert os.path.exists(test_file), f"Test API file missing: {test_file}"

    try:
        subprocess.check_output(['pytest', test_file], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        assert False, f"Tests in {test_file} failed. Output:\n{e.output.decode('utf-8')}"