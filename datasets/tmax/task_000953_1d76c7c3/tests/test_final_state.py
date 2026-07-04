# test_final_state.py

import os
import json
import urllib.request
import pytest

def test_result_json():
    result_path = '/home/user/api_project/result.json'
    assert os.path.isfile(result_path), f"File {result_path} does not exist. Did you run your test script?"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} does not contain valid JSON.")

    expected = [
      {"id": 1, "name": "Alpha"},
      {"id": 2, "name": "Bravo"},
      {"id": 3, "name": "Charlie"},
      {"id": 4, "name": "Delta"},
      {"id": 5, "name": "Echo"}
    ]

    assert data == expected, f"Content of {result_path} did not match the expected sorted list of objects."

def test_server_py_fixed():
    server_path = '/home/user/api_project/server.py'
    assert os.path.isfile(server_path), f"File {server_path} is missing."

    with open(server_path, 'r') as f:
        content = f.read()

    assert 'cmp=' not in content, "Python 2 'cmp=' sort idiom was not removed from server.py."
    assert 'iteritems()' not in content, "Python 2 'iteritems()' idiom was not removed from server.py."

def test_nginx_conf_fixed():
    nginx_path = '/home/user/api_project/nginx.conf'
    assert os.path.isfile(nginx_path), f"File {nginx_path} is missing."

    with open(nginx_path, 'r') as f:
        content = f.read()

    assert 'proxy_pass http://127.0.0.1:8080;' in content, "Nginx configuration does not proxy to the correct port (8080)."

def test_services_running_and_proxy_working():
    url = "http://127.0.0.1:8000/api/merge_sort"
    payload = {
        "list1": [{"id": 5, "name": "Echo"}, {"id": 1, "name": "Alpha"}, {"id": 3, "name": "Charlie"}],
        "list2": [{"id": 4, "name": "Delta"}, {"id": 2, "name": "Bravo"}]
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected status code 200, got {response.status}"
            resp_data = json.loads(response.read().decode('utf-8'))
            expected = [
                {"id": 1, "name": "Alpha"},
                {"id": 2, "name": "Bravo"},
                {"id": 3, "name": "Charlie"},
                {"id": 4, "name": "Delta"},
                {"id": 5, "name": "Echo"}
            ]
            assert resp_data == expected, "The API did not return the correctly sorted list when accessed through the reverse proxy."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the Nginx proxy at {url}. Are Nginx and the Python server running? Error: {e}")