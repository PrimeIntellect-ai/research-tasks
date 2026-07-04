# test_final_state.py
import json
import os
import urllib.request
import urllib.error

def test_setup_py_exists():
    """Verify that the setup.py file exists in the correct location."""
    setup_path = "/home/user/math_ops/setup.py"
    assert os.path.isfile(setup_path), f"Expected {setup_path} to exist."

def test_test_results_log():
    """Verify the contents of the test_results.log file."""
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Expected {log_path} to exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {log_path}, found {len(lines)}."

    try:
        res1 = json.loads(lines[0])
        res2 = json.loads(lines[1])
        res3 = json.loads(lines[2])
    except json.JSONDecodeError:
        assert False, "Failed to parse lines in test_results.log as JSON."

    assert res1.get("result") == [-2, 3, 5, 10], f"Sort result incorrect: {res1}"
    assert res2.get("result") == [1, 2, 5, 5, 8, 9], f"Merge result incorrect: {res2}"
    assert res3.get("result") == [1, 2, 5, 6], f"Diff result incorrect: {res3}"

def test_nginx_proxy_active():
    """Verify that Nginx is running on port 8080 and proxying to the Flask app."""
    url = "http://127.0.0.1:8080/api/sort"
    data = json.dumps({"data": []}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = json.loads(response.read().decode('utf-8'))
            assert "result" in body, "Expected 'result' key in response JSON."
            assert body["result"] == [], f"Expected empty array for empty sort, got {body['result']}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx on port 8080 or Flask app: {e}"