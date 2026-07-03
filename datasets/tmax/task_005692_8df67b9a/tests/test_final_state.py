# test_final_state.py

import os
import json
import urllib.request
import pytest
import importlib

def test_shared_library_exists():
    lib_path = "/home/user/workspace/token_api/lib/libcorealgo.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist. Did you compile it?"

def test_api_output_json():
    output_path = "/home/user/api_output.json"
    assert os.path.isfile(output_path), f"API output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    assert data.get("status") == "success", f"Expected status 'success' in {output_path}, got {data.get('status')}"
    assert data.get("seed") == 12, f"Expected seed 12 in {output_path}, got {data.get('seed')}"

    # Compute expected token
    seed = 12
    for _ in range(1000):
        seed = (seed * 13 + 17) % 9973
    expected_token = seed

    assert data.get("token") == expected_token, f"Expected token {expected_token} in {output_path}, got {data.get('token')}"

def test_python_module_import_and_rpath():
    # We should be able to import token_ext directly.
    # If rpath is not set correctly, this will fail with an ImportError (cannot open shared object file)
    # unless LD_LIBRARY_PATH is set, which we can clear for this test just to be sure.

    original_ld_path = os.environ.get("LD_LIBRARY_PATH")
    if "LD_LIBRARY_PATH" in os.environ:
        del os.environ["LD_LIBRARY_PATH"]

    try:
        import token_ext

        # Test the generate_token function
        seed = 12
        for _ in range(1000):
            seed = (seed * 13 + 17) % 9973
        expected_token = seed

        assert token_ext.generate_token(12) == expected_token, "token_ext.generate_token(12) returned incorrect value."
    except ImportError as e:
        pytest.fail(f"Failed to import token_ext. This is likely due to missing rpath in setup.py. Error: {e}")
    finally:
        if original_ld_path is not None:
            os.environ["LD_LIBRARY_PATH"] = original_ld_path

def test_api_is_running():
    # The task requires the API to be running on port 8080
    url = "http://localhost:8080/generate?seed=5"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"API returned status {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("status") == "success", "API did not return status 'success'."
            assert data.get("seed") == 5, "API did not return the correct seed."
    except Exception as e:
        pytest.fail(f"Could not connect to the API on port 8080 or it returned an error. Is app.py running? Error: {e}")