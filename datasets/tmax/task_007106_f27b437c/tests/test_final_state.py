# test_final_state.py
import os
import sys
import subprocess
import importlib.util

def test_rust_ext_fixed_and_installed():
    # Verify that rust_ext is installed and works correctly
    try:
        import rust_ext
    except ImportError:
        assert False, "rust_ext module is not installed or cannot be imported. Did you run `maturin develop`?"

    # Check if the function works correctly
    try:
        result = rust_ext.process_string("test")
        assert result == "testtest", f"rust_ext.process_string('test') returned '{result}', expected 'testtest'"
    except Exception as e:
        assert False, f"rust_ext.process_string failed with error: {e}"

def test_property_based_test_exists_and_passes():
    test_file = "/home/user/workspace/test_ext.py"
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."

    with open(test_file, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "The test file does not seem to use the hypothesis library."
    assert "test_process_string_property" in content, "The test function 'test_process_string_property' is missing."

    # Run pytest on the file to ensure it passes
    result = subprocess.run([sys.executable, "-m", "pytest", test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest failed on {test_file}:\n{result.stdout}\n{result.stderr}"

def test_nginx_config_exists_and_valid():
    conf_file = "/home/user/workspace/nginx.conf"
    assert os.path.isfile(conf_file), f"Nginx config file {conf_file} does not exist."

    with open(conf_file, "r") as f:
        content = f.read()

    assert "8080" in content, "Nginx config does not seem to listen on port 8080."
    assert "127.0.0.1:5000" in content, "Nginx config does not seem to proxy to 127.0.0.1:5000."
    assert "pid" in content, "Nginx config does not specify a pid directive."
    assert "worker_processes 1" in content or "worker_processes  1" in content, "Nginx config does not set worker_processes to 1."
    assert "events" in content, "Nginx config does not contain an events block."

def test_response_txt_contains_correct_string():
    response_file = "/home/user/workspace/response.txt"
    assert os.path.isfile(response_file), f"Response file {response_file} does not exist."

    with open(response_file, "r") as f:
        content = f.read().strip()

    expected = "platformplatform"
    assert content == expected, f"Expected response.txt to contain '{expected}', but found '{content}'"