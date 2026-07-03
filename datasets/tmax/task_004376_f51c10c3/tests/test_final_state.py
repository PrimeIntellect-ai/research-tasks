# test_final_state.py
import os
import json
import urllib.request
import pytest

def test_libcompute_so_exists():
    assert os.path.isfile('/home/user/workspace/libcompute.so'), "Shared library libcompute.so was not compiled or is missing."

def test_result_log_content():
    log_path = '/home/user/workspace/result.log'
    assert os.path.isfile(log_path), "result.log is missing."
    with open(log_path, 'r') as f:
        content = f.read().strip()
    assert content == "65.0000", f"result.log contains incorrect value: {content}, expected 65.0000"

def test_services_running_and_correct():
    payload = [{"id": 2, "value": 3.0}, {"id": 3, "value": 4.0}]
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/api/process', data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Content-Length', str(len(data)))

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_body = response.read().decode('utf-8').strip()
            assert res_body == "18.0000", f"Expected Nginx/Python pipeline to return 18.0000 for test payload, but got {res_body}"
    except Exception as e:
        pytest.fail(f"Failed to communicate with Nginx or Python app: {e}")