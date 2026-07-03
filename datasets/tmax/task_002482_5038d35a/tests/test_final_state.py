# test_final_state.py

import os
import json
import socket
import urllib.request
import urllib.error
import pytest

PROJECT_DIR = "/home/user/project"

def test_processor_cpp_fixed():
    filepath = os.path.join(PROJECT_DIR, "processor.cpp")
    assert os.path.isfile(filepath), f"{filepath} does not exist"

    with open(filepath, "r") as f:
        content = f.read()

    assert 'extern "C"' in content, "processor.cpp is missing 'extern \"C\"' linkage"
    assert "std::string sort_items" not in content, "processor.cpp should not return std::string directly"

def test_shared_library_compiled():
    so_path = os.path.join(PROJECT_DIR, "libprocessor.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} was not compiled"

def test_server_py_fixed():
    filepath = os.path.join(PROJECT_DIR, "server.py")
    assert os.path.isfile(filepath), f"{filepath} does not exist"

    with open(filepath, "r") as f:
        content = f.read()

    # Check that restype is configured and not commented out
    lines = content.split('\n')
    restype_configured = any('lib.sort_items.restype' in line and not line.strip().startswith('#') for line in lines)
    assert restype_configured, "server.py is missing the proper restype configuration for lib.sort_items"

def test_test_endpoint_sh_exists():
    filepath = os.path.join(PROJECT_DIR, "test_endpoint.sh")
    assert os.path.isfile(filepath), f"{filepath} does not exist"

def test_final_output_json():
    filepath = os.path.join(PROJECT_DIR, "final_output.json")
    assert os.path.isfile(filepath), f"{filepath} does not exist"

    with open(filepath, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail("final_output.json does not contain valid JSON")

    expected = [{"id": 1, "val": "A"}, {"id": 2, "val": "B"}, {"id": 3, "val": "C"}]
    assert data == expected, f"final_output.json content is incorrect. Got: {content}"

def test_reverse_proxy_and_server_running():
    # Test if port 8000 is accepting connections and properly forwarding to the server
    payload = b'[{"id": 3, "val": "C"}, {"id": 1, "val": "A"}, {"id": 2, "val": "B"}]'
    req = urllib.request.Request("http://127.0.0.1:8000", data=payload, method="POST")
    req.add_header('Content-Length', str(len(payload)))

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            resp_data = response.read().decode('utf-8')
            try:
                parsed_resp = json.loads(resp_data)
                expected = [{"id": 1, "val": "A"}, {"id": 2, "val": "B"}, {"id": 3, "val": "C"}]
                assert parsed_resp == expected, "Reverse proxy server did not return the correctly sorted JSON"
            except json.JSONDecodeError:
                pytest.fail("Server did not return valid JSON")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to reverse proxy on port 8000 or server on port 8080: {e}")
    except socket.timeout:
        pytest.fail("Request to port 8000 timed out")