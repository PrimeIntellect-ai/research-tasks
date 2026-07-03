# test_final_state.py
import urllib.request
import urllib.parse
import urllib.error
import base64
import zlib
import json
import os
import ast
import tempfile
import pytest

APP_FILE = "/home/user/polybuild/src/app.py"
SERVER_FILE = "/home/user/polybuild/server.py"

def test_app_py_imports_sorted():
    """Check that the imports in app.py are sorted alphabetically."""
    assert os.path.exists(APP_FILE), f"Target file {APP_FILE} is missing."
    with open(APP_FILE, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)

    assert imports == sorted(imports), f"Imports in {APP_FILE} are not strictly alphabetical. Found: {imports}"

def test_server_file_exists():
    """Check that the server.py file exists."""
    assert os.path.exists(SERVER_FILE), f"Server file {SERVER_FILE} is missing."

def test_server_valid_request():
    """Test the server with a valid request for the fixed app.py."""
    target_bytes = APP_FILE.encode('iso-8859-1')
    target_b64 = base64.b64encode(target_bytes).decode('ascii')
    crc = zlib.crc32(target_bytes)

    url = f"http://127.0.0.1:8080/validate?target={urllib.parse.quote(target_b64)}&crc={crc}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get('status') == 'pass', f"Expected status 'pass', got {data.get('status')}"
            assert 'peak_memory_bytes' in data, "Missing 'peak_memory_bytes' in response"
            assert isinstance(data['peak_memory_bytes'], int), "'peak_memory_bytes' must be an integer"
    except urllib.error.URLError as e:
        pytest.fail(f"Server is not running or unreachable on 127.0.0.1:8080. Error: {e}")

def test_server_invalid_crc():
    """Test the server with an invalid CRC."""
    target_bytes = APP_FILE.encode('iso-8859-1')
    target_b64 = base64.b64encode(target_bytes).decode('ascii')
    crc = zlib.crc32(target_bytes) + 1 # Invalid CRC

    url = f"http://127.0.0.1:8080/validate?target={urllib.parse.quote(target_b64)}&crc={crc}"

    try:
        urllib.request.urlopen(url)
        pytest.fail("Expected HTTP 400 Bad Request for invalid CRC, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Server is not running or unreachable on 127.0.0.1:8080. Error: {e}")

def test_server_unsorted_imports():
    """Test the server with a file that has unsorted imports."""
    # Create a temporary file with unsorted imports
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("import sys\nimport os\n")
        temp_path = f.name

    try:
        target_bytes = temp_path.encode('iso-8859-1')
        target_b64 = base64.b64encode(target_bytes).decode('ascii')
        crc = zlib.crc32(target_bytes)

        url = f"http://127.0.0.1:8080/validate?target={urllib.parse.quote(target_b64)}&crc={crc}"

        try:
            urllib.request.urlopen(url)
            pytest.fail("Expected HTTP 406 Not Acceptable for unsorted imports, but request succeeded.")
        except urllib.error.HTTPError as e:
            assert e.code == 406, f"Expected HTTP 406, got {e.code}"
        except urllib.error.URLError as e:
            pytest.fail(f"Server is not running or unreachable on 127.0.0.1:8080. Error: {e}")
    finally:
        os.remove(temp_path)