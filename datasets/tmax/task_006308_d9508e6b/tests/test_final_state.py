# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_rust_executable_exists():
    executable_path = '/home/user/rust_encoder/target/debug/rust_encoder'
    assert os.path.isfile(executable_path), f"The rust executable was not found at {executable_path}. Did you run 'cargo build'?"
    assert os.access(executable_path, os.X_OK), f"The file at {executable_path} is not executable."

def test_python_server_fixed():
    server_py_path = '/home/user/server.py'
    assert os.path.isfile(server_py_path), "The server.py file is missing."

    with open(server_py_path, 'r') as f:
        content = f.read()

    assert "qs.get('shift'" in content, "The query parameter parsing bug in server.py does not appear to be fixed. It should extract 'shift' instead of 'shft'."

def test_server_is_running_and_responds():
    try:
        url = "http://127.0.0.1:8080/encode?msg=Test&shift=1"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            assert status == 200, f"Expected HTTP 200 OK, got {status}"
            body = response.read().decode('utf-8')
            assert body == "Uftu", f"Expected 'Uftu' for msg=Test&shift=1, got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"The server does not appear to be running on 127.0.0.1:8080 or failed to respond: {e}")

def test_artifact_file_contents():
    artifact_path = '/home/user/artifact.txt'
    assert os.path.isfile(artifact_path), f"The artifact file at {artifact_path} is missing."

    with open(artifact_path, 'r') as f:
        content = f.read()

    expected_content = "Jpnw}"
    assert content == expected_content, f"The artifact file content is incorrect. Expected '{expected_content}', but got '{content}'."